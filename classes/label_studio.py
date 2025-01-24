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
            labels_element = ET.SubElement(view, "Labels", name="videoLabels", toName="video", allowEmpty="true")

            # Iterate over the labels and create <Label> elements as children of <Labels>
            for label_name in labels:
                # Add <Label> element as a child of <Labels>
                ET.SubElement(labels_element, "Label", value=label_name, background="#ff00dd")

            # Create <Video> element with attributes
            ET.SubElement(view, "Video", name="video", value="$video", framerate=f"{fps}")

            # Create <VideoRectangle> element with attributes
            ET.SubElement(view, "VideoRectangle", name="box", toName="video")

            # Convert the tree to a string
            xml_string = ET.tostring(view, encoding="unicode")

            # Add pretty formatting (optional, for readability)
            dom = xml.dom.minidom.parseString(xml_string)
            pretty_xml_string = dom.toprettyxml()

            # Log and return the formatted XML
            current_app.logger.info(f"{__class__.__name__} --- LABEL_CONFIG_VIDEO_XML: {pretty_xml_string}")
            return { "status": "SUCCESS", "data": pretty_xml_string }

        except Exception as e:
            return { "status": "FAILED", "error": str(e) }
