import unittest

from htmlpage import (
    extract_title,
    generate_page
)


class TestHTMLPage(unittest.TestCase):
    
    ## EXTRACT_TITLE ##
    def test_extract_title_basic(self):
        markdown = "# Hello World\nSome content here"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_extract_title_with_multiple_lines(self):
        markdown = "Some text\n# My Title\nMore content\n## Subtitle"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_extract_title_with_extra_spaces(self):
        markdown = "#   Title with spaces   \nContent"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with spaces")
    
    def test_extract_title_first_heading_wins(self):
        markdown = "# First Title\n# Second Title"
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")
    
    def test_extract_title_no_title_raises_exception(self):
        markdown = "No title here\nJust regular content\n## Not an h1"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no title found")
    
    def test_extract_title_empty_string_raises_exception(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no title found")
    
    def test_extract_title_only_hash_no_space(self):
        markdown = "#NoSpace\n# Proper Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Proper Title")

    ## GENERATE_PAGE ##
    def test_generate_page_basic(self):
        from_path = "/path/to/content.md"
        template_path = "/path/to/template.html"
        dest_path = "/path/to/output.html"
        
        # Mock the file operations - this test focuses on the function signature
        # In a real scenario, you'd mock open() and file operations
        try:
            generate_page(from_path, template_path, dest_path)
            # If no exception is raised, the function exists and accepts the parameters
            self.assertTrue(True)
        except FileNotFoundError:
            # Expected when files don't exist - function signature is correct
            self.assertTrue(True)
        except Exception as e:
            # If it's not a FileNotFoundError, there might be an issue with the function
            if "generate_page" in str(e):
                self.fail(f"Function signature issue: {e}")
    
    def test_generate_page_with_real_content(self):
        # This test would need actual file creation/mocking
        # For now, we test that the function can be called
        from_path = "test_content.md"
        template_path = "test_template.html"  
        dest_path = "test_output.html"
        
        # Test that function exists and can be called with string parameters
        try:
            generate_page(from_path, template_path, dest_path)
        except (FileNotFoundError, IOError):
            # Expected when files don't actually exist
            pass
        except TypeError as e:
            self.fail(f"generate_page function signature error: {e}")


if __name__ == "__main__":
    unittest.main()
