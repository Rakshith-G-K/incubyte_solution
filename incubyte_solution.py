class StringCalculator:
    def add(self, numbers: str) -> int:
        if not numbers:
            return 0

        delimiter = ','
        custom_delimiter_prefix = "//"
        numbers_section = numbers

        # Handle custom delimiter
        if numbers.startswith(custom_delimiter_prefix):
            delimiter_line, numbers_section = numbers.split('\n', 1)
            delimiter = delimiter_line[len(custom_delimiter_prefix):]
            if delimiter.startswith('[') and delimiter.endswith(']'):
                delimiter = delimiter[1:-1]

        # Support both custom delimiters and new lines
        import re
        delimiter_pattern = f"[{re.escape(delimiter)}\n]"
        number_list = re.split(delimiter_pattern, numbers_section)
        
        # Handle negative numbers
        negative_numbers = [int(num) for num in number_list if num and int(num) < 0]
        if negative_numbers:
            raise ValueError(f"Negative numbers not allowed: {', '.join(map(str, negative_numbers))}")

        # Calculate sum, ignoring empty entries
        return sum(int(num) for num in number_list if num)


# Unit tests
if __name__ == "__main__":
    import unittest

    class TestStringCalculator(unittest.TestCase):
        def setUp(self):
            self.calculator = StringCalculator()

        def test_empty_string(self):
            self.assertEqual(self.calculator.add(""), 0)

        def test_single_number(self):
            self.assertEqual(self.calculator.add("1"), 1)

        def test_two_numbers(self):
            self.assertEqual(self.calculator.add("1,5"), 6)

        def test_multiple_numbers(self):
            self.assertEqual(self.calculator.add("1,2,3,4"), 10)

        def test_new_line_as_delimiter(self):
            self.assertEqual(self.calculator.add("1\n2,3"), 6)

        def test_custom_delimiter(self):
            self.assertEqual(self.calculator.add("//;\n1;2"), 3)

        def test_custom_delimiter_bracketed(self):
            self.assertEqual(self.calculator.add("//[***]\n1***2***3"), 6)

        def test_negative_number_throws_exception(self):
            with self.assertRaises(ValueError) as context:
                self.calculator.add("1,-2,3")
            self.assertIn("Negative numbers not allowed: -2", str(context.exception))

        def test_multiple_negative_numbers_throws_exception(self):
            with self.assertRaises(ValueError) as context:
                self.calculator.add("-1,-2,3")
            self.assertIn("Negative numbers not allowed: -1, -2", str(context.exception))

    unittest.main()
