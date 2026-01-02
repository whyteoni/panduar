import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_node_images,
    split_node_links,
    text_to_textnodes
)

class TestTextNode(unittest.TestCase):

    ####################
    ## TEXTNODE CLASS ##
    ####################

    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_provided(self):
        url = "https://127.0.0.1"
        node = TextNode("This is a text node", TextType.LINK,url)
        self.assertEqual(node.url, url)

    def test_url_default(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_texttypes(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node1,node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("Different text", TextType.TEXT)
        node2 = TextNode("Another text", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://site1.com")
        node2 = TextNode("Link text", TextType.LINK, "https://site2.com")
        self.assertNotEqual(node1, node2)

    def test_equal_with_same_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_text_node_repr(self):
        node = TextNode("Test text", TextType.BOLD, "https://example.com")
        expected = "TextNode(Test text, bold, https://example.com)"
        self.assertEqual(repr(node), expected)

    #####################################
    ## TEXT_NODE_TO_HTML_NODE FUNCTION ##
    #####################################

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_convert_bold(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_convert_italic(self):
        text_node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),"<i>Italic text</i>")

    def test_convert_code(self):
        code = TextNode("Code block", TextType.CODE)
        html_node = text_node_to_html_node(code)
        self.assertEqual(html_node.to_html(), "<code>Code block</code>")

    def test_convert_link(self):
        link_node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")

    def test_none_url_conversion(self):
        node = TextNode("Text", TextType.TEXT, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)

    ######################
    ## TEXTNODE STYLING ##
    ######################

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bolded")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "more bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_split_nodes_multiple_nodes(self):
        node1 = TextNode("First **bold** text", TextType.TEXT)
        node2 = TextNode("Second **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[4].text, "bold")

    ###################################
    ## EXTRACT MARKDOWN IMAGES/LINKS ##
    ###################################

    def test_extract_markdown_images_single(self):
        text = "This is text with an ![alt text](https://example.com/image.png) image"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "https://example.com/image.png"))

    def test_extract_markdown_images_multiple(self):
        text = "Here's ![first](image1.png) and ![second](image2.jpg) images"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("first", "image1.png"))
        self.assertEqual(images[1], ("second", "image2.jpg"))

    def test_extract_markdown_images_none(self):
        text = "This text has no images"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
        self.assertEqual(images, [])

    def test_extract_markdown_images_empty_alt(self):
        text = "Image with empty alt text ![](image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("", "image.png"))

    def test_extract_markdown_links_single(self):
        text = "This is text with a [link](https://example.com) to a site"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "https://example.com"))

    def test_extract_markdown_links_multiple(self):
        text = "Visit [Google](https://google.com) and [GitHub](https://github.com)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("Google", "https://google.com"))
        self.assertEqual(links[1], ("GitHub", "https://github.com"))

    def test_extract_markdown_links_none(self):
        text = "This text has no links"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)
        self.assertEqual(links, [])

    def test_extract_markdown_links_empty_text(self):
        text = "Link with empty text [](https://example.com)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("", "https://example.com"))

    def test_extract_mixed_images_and_links(self):
        text = "Here's a [link](https://example.com) and an ![image](pic.jpg)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(len(links), 1)
        self.assertEqual(images[0], ("image", "pic.jpg"))
        self.assertEqual(links[0], ("link", "https://example.com"))

    def test_extract_images_ignores_links(self):
        text = "This has [link](url.com) but no images"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_extract_links_ignores_images(self):
        text = "This has ![image](pic.png) but no links"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    ###############################
    ## SPLIT NODES: IMAGES/LINKS ##
    ###############################

    def test_split_node_images_single(self):
        node = TextNode("This is text with an ![alt text](https://example.com/image.png) image", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image.png")
        self.assertEqual(new_nodes[2].text, " image")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_node_images_multiple(self):
        node = TextNode("Here's ![first](image1.png) and ![second](image2.jpg) images", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Here's ")
        self.assertEqual(new_nodes[1].text, "first")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "image1.png")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "second")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "image2.jpg")
        self.assertEqual(new_nodes[4].text, " images")

    def test_split_node_images_no_images(self):
        node = TextNode("This text has no images", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_node_images_empty_alt(self):
        node = TextNode("Image with empty alt ![](image.png) text", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "image.png")

    def test_split_node_images_multiple_nodes(self):
        node1 = TextNode("First ![image1](pic1.png) node", TextType.TEXT)
        node2 = TextNode("Second ![image2](pic2.jpg) node", TextType.TEXT)
        new_nodes = split_node_images([node1, node2])
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[1].text, "image1")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[4].text, "image2")
        self.assertEqual(new_nodes[4].text_type, TextType.IMAGE)

    def test_split_node_links_single(self):
        node = TextNode("This is text with a [link](https://example.com) to a site", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " to a site")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_node_links_multiple(self):
        node = TextNode("Visit [Google](https://google.com) and [GitHub](https://github.com) sites", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Visit ")
        self.assertEqual(new_nodes[1].text, "Google")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://google.com")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "GitHub")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://github.com")
        self.assertEqual(new_nodes[4].text, " sites")

    def test_split_node_links_no_links(self):
        node = TextNode("This text has no links", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_node_links_empty_text(self):
        node = TextNode("Link with empty text [](https://example.com) here", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")

    def test_split_node_links_multiple_nodes(self):
        node1 = TextNode("First [link1](url1.com) node", TextType.TEXT)
        node2 = TextNode("Second [link2](url2.com) node", TextType.TEXT)
        new_nodes = split_node_links([node1, node2])
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[1].text, "link1")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[4].text, "link2")
        self.assertEqual(new_nodes[4].text_type, TextType.LINK)

    def test_split_node_images_ignores_links(self):
        node = TextNode("This has [link](url.com) but no images", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_node_links_ignores_images(self):
        node = TextNode("This has ![image](pic.png) but no links", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    ##################################
    ## TEXT TO TEXTNODES CONVERSION ##
    ##################################

    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_link(self):
        text = "This is a [link](https://example.com) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_image(self):
        text = "This is an ![image](https://example.com/pic.jpg) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/pic.jpg")
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_multiple_formatting(self):
        text = "This is **bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 6)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " and ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)

    def test_text_to_textnodes_mixed_images_and_links(self):
        text = "Here's a [link](https://example.com) and an ![image](pic.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text, "Here's a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " and an ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "image")
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(nodes[3].url, "pic.jpg")

    def test_text_to_textnodes_complex_formatting(self):
        text = "This is **bold with `code` inside** and _italic with ![image](pic.png) inside_"
        nodes = text_to_textnodes(text)
        # This should handle nested formatting appropriately
        self.assertGreater(len(nodes), 1)
        # At minimum, we should have some bold and italic nodes
        bold_nodes = [n for n in nodes if n.text_type == TextType.BOLD]
        italic_nodes = [n for n in nodes if n.text_type == TextType.ITALIC]
        self.assertGreater(len(bold_nodes), 0)
        self.assertGreater(len(italic_nodes), 0)

    def test_text_to_textnodes_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 0)

    def test_text_to_textnodes_only_formatting(self):
        text = "**bold**"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_text_to_textnodes_multiple_same_formatting(self):
        text = "This is **bold** and **more bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[3].text, "more bold")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
