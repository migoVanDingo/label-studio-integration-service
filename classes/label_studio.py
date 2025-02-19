import xml.etree.ElementTree as ET
import xml.dom.minidom

from flask import current_app


class LabelStudio:
    @staticmethod
    def create_label_config_video(labels: list, fps: int):
        try:
            # Create the root element <View>
            view = ET.Element("View")

            # Create <Labels> element with attributes
            labels_element = ET.SubElement(
                view, "Labels", name="videoLabels", toName="video", allowEmpty="true")
            color_dict = {
                0: "#FF5733",  1: "#33FF57",  2: "#3357FF",  3: "#F3FF33",  4: "#FF33A8",
                5: "#33FFF5",  6: "#A833FF",  7: "#FF8C33",  8: "#33FF8C",  9: "#8C33FF",
                10: "#FF336E", 11: "#36FF33", 12: "#33A8FF", 13: "#FF5733", 14: "#33FFBD",
                15: "#FFBD33", 16: "#BD33FF", 17: "#33D4FF", 18: "#D433FF", 19: "#FF3336"
            }

            # Iterate over the labels and create <Label> elements as children of <Labels>
            for idx, label_name in enumerate(labels):
                # Assign a color from the dictionary, cycling through if there are more labels than colors
                color = color_dict[idx % len(color_dict)]

                # Add <Label> element as a child of <Labels>
                ET.SubElement(labels_element, "Label", value=label_name, background=color)

            # Create <Video> element with attributes
            ET.SubElement(view, "Video", name="video",
                          value="$video", framerate=f"{fps}")

            # Create <VideoRectangle> element with attributes
            ET.SubElement(view, "VideoRectangle", name="box", toName="video")

            # Convert the tree to a string
            xml_string = ET.tostring(view, encoding="unicode")

            # Add pretty formatting (optional, for readability)
            dom = xml.dom.minidom.parseString(xml_string)
            pretty_xml_string = dom.toprettyxml()

            # Log and return the formatted XML
            current_app.logger.info(
                f"{__class__.__name__} --- LABEL_CONFIG_VIDEO_XML: {pretty_xml_string}")
            return {"status": "SUCCESS", "data": pretty_xml_string}

        except Exception as e:
            return {"status": "FAILED", "error": str(e)}
