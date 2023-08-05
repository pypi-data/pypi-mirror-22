# Easily capture stdout/stderr of the current process and subprocesses.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: November 12, 2016
# URL: https://capturer.readthedocs.io

"""Test suite for the `capturer` package."""

# Standard library modules.
import os
import random
import string
import subprocess
import sys
import tempfile
import time
import unittest

# The module we're testing.
from capturer import interpret_carriage_returns, CaptureOutput, Stream


class CapturerTestCase(unittest.TestCase):

    """Container for the `capturer` test suite."""

    def test_carriage_return_interpretation(self):
        """Sanity check the results of interpret_carriage_returns()."""
        # Simple output should pass through unharmed.
        assert interpret_carriage_returns('foo') == ['foo']
        # Simple output should pass through unharmed.
        assert interpret_carriage_returns('foo\nbar') == ['foo', 'bar']
        # Carriage returns and preceding substrings should be stripped.
        assert interpret_carriage_returns('foo\rbar\nbaz') == ['bar', 'baz']
        # Trailing empty lines should be stripped.
        assert interpret_carriage_returns('foo\nbar\nbaz\n\n\n') == ['foo', 'bar', 'baz']

    def test_error_handling(self):
        """Test error handling code paths."""
        # Nested CaptureOutput.start_capture() calls should raise an exception.
        capturer = CaptureOutput()
        capturer.start_capture()
        try:
            self.assertRaises(TypeError, capturer.start_capture)
        finally:
            # Make sure not to start swallowing output here ;-).
            capturer.finish_capture()
        # Nested Stream.redirect() calls should raise an exception.
        stream = Stream(sys.stdout.fileno())
        stream.redirect(sys.stderr.fileno())
        self.assertRaises(TypeError, stream.redirect, sys.stderr.fileno())

    def test_stdout_capture_same_process(self):
        """Test standard output capturing from the same process."""
        expected_stdout = random_string()
        with CaptureOutput() as capturer:
            print(expected_stdout)
            assert expected_stdout in capturer.get_lines()

    def test_stderr_capture_same_process(self):
        """Test standard error capturing from the same process."""
        expected_stderr = random_string()
        with CaptureOutput() as capturer:
            sys.stderr.write(expected_stderr + "\n")
            assert expected_stderr in capturer.get_lines()

    def test_combined_capture_same_process(self):
        """Test combined standard output and error capturing from the same process."""
        expected_stdout = random_string()
        expected_stderr = random_string()
        with CaptureOutput() as capturer:
            sys.stdout.write(expected_stdout + "\n")
            sys.stderr.write(expected_stderr + "\n")
            assert expected_stdout in capturer.get_lines()
            assert expected_stderr in capturer.get_lines()

    def test_stdout_capture_subprocess(self):
        """Test standard output capturing from subprocesses."""
        expected_stdout = random_string()
        with CaptureOutput() as capturer:
            subprocess.call([
                sys.executable,
                '-c',
                ';'.join([
                    'import sys',
                    'sys.stdout.write(%r)' % (expected_stdout + '\n'),
                ]),
            ])
            assert expected_stdout in capturer.get_lines()

    def test_stderr_capture_subprocess(self):
        """Test standard error capturing from subprocesses."""
        expected_stderr = random_string()
        with CaptureOutput() as capturer:
            subprocess.call([
                sys.executable,
                '-c',
                ';'.join([
                    'import sys',
                    'sys.stderr.write(%r)' % (expected_stderr + '\n'),
                ]),
            ])
            assert expected_stderr in capturer.get_lines()

    def test_combined_capture_subprocess(self):
        """Test combined standard output and error capturing from subprocesses."""
        expected_stdout = random_string()
        expected_stderr = random_string()
        with CaptureOutput() as capturer:
            subprocess.call([
                sys.executable,
                '-c',
                ';'.join([
                    'import sys',
                    'sys.stdout.write(%r)' % (expected_stdout + '\n'),
                    'sys.stderr.write(%r)' % (expected_stderr + '\n'),
                ]),
            ])
            assert expected_stdout in capturer.get_lines()
            assert expected_stderr in capturer.get_lines()

    def test_combined_current_and_subprocess(self):
        """Test combined standard output and error capturing from the same process and subprocesses."""
        # Some unique strings that are not substrings of each other.
        cur_stdout_1 = "Some output from Python's print statement"
        cur_stdout_2 = "Output from Python's sys.stdout.write() method"
        cur_stdout_3 = "More output from Python's print statement"
        cur_stderr = "Output from Python's sys.stderr.write() method"
        sub_stderr = "Output from subprocess stderr stream"
        sub_stdout = "Output from subprocess stdout stream"
        with CaptureOutput() as capturer:
            # Emit multiple lines on both streams from current process and subprocess.
            print(cur_stdout_1)
            sys.stderr.write("%s\n" % cur_stderr)
            subprocess.call(["sh", "-c", "echo %s 1>&2" % sub_stderr])
            subprocess.call(["echo", sub_stdout])
            sys.stdout.write("%s\n" % cur_stdout_2)
            print(cur_stdout_3)
            # Verify that all of the expected lines were captured.
            assert all(l in capturer.get_lines() for l in (
                cur_stdout_1, cur_stderr, sub_stderr,
                sub_stdout, cur_stdout_2, cur_stdout_3,
            ))

    def test_partial_read(self):
        """Test that partial reading works as expected."""
        # This test method uses retry logic because `partial=True' makes these
        # tests prone to race conditions (this is the whole reason why
        # `partial=False' by default :-).
        initial_part = random_string()
        later_part = random_string()
        with CaptureOutput() as capturer:
            sys.stderr.write("%s\n" % initial_part)
            retry(lambda: initial_part in capturer.get_lines(partial=True))
            sys.stderr.write("%s\n" % later_part)
            retry(lambda: later_part in capturer.get_lines(partial=True))

    def test_non_interpreted_lines_capture(self):
        """Test that interpretation of special characters can be disabled."""
        expected_output = random_string()
        with CaptureOutput() as capturer:
            print(expected_output)
            assert expected_output in capturer.get_lines(interpreted=False)

    def test_text_capture(self):
        """Test that capturing of all output as a single string is supported."""
        expected_output = random_string()
        with CaptureOutput() as capturer:
            print(expected_output)
            assert expected_output in capturer.get_text()

    def test_save_to_path(self):
        """Test that captured output can be stored in a file."""
        expected_output = random_string()
        with CaptureOutput() as capturer:
            print(expected_output)
            fd, temporary_file = tempfile.mkstemp()
            try:
                capturer.save_to_path(temporary_file)
                with open(temporary_file, 'r') as handle:
                    assert expected_output in handle.read()
            finally:
                os.unlink(temporary_file)

    def test_unmerged_capture(self):
        """Test that standard output and error can be captured separately."""
        expected_stdout = random_string()
        expected_stderr = random_string()
        with CaptureOutput(merged=False) as capturer:
            sys.stdout.write(expected_stdout + "\n")
            sys.stderr.write(expected_stderr + "\n")
            assert expected_stdout in capturer.stdout.get_lines()
            assert expected_stderr in capturer.stderr.get_lines()


def random_string():
    """Generate a random string."""
    length = random.randint(25, 100)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def retry(func, timeout=10):
    """Retry a function until it returns True or the timeout passes."""
    time_started = time.time()
    while (time.time() - time_started) < timeout:
        if func():
            return
    assert False, "Timeout expired but function never passed all assertions!"


if __name__ == '__main__':
    unittest.main()
