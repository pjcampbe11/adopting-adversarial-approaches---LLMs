import argparse
import zipfile
import os

def inject_hidden_prompt(doc_path, doc_type, location, payload, is_file):
    # Determine the file paths based on document type and location
    file_paths = {
        'word': {
            'rels': '_rels/.rels',
            'docProps': 'docProps/core.xml',
            'document': 'word/document.xml',
            'fontTable': 'word/fontTable.xml',
            'settings': 'word/settings.xml',
            'styles': 'word/styles.xml',
            'theme': 'word/theme/theme1.xml',
            'webSettings': 'word/webSettings.xml',
            'docRels': 'word/_rels/document.xml.rels',
            'contentTypes': '[Content_Types].xml'
        },
        'excel': {
            'rels': '_rels/.rels',
            'docProps': 'docProps/core.xml',
            'workbook': 'xl/workbook.xml',
            'styles': 'xl/styles.xml',
            'sharedStrings': 'xl/sharedStrings.xml',
            'theme': 'xl/theme/theme1.xml',
            'sheet1': 'xl/worksheets/sheet1.xml',
            'workbookRels': 'xl/_rels/workbook.xml.rels',
            'contentTypes': '[Content_Types].xml'
        },
        'powerpoint': {
            'rels': '_rels/.rels',
            'docProps': 'docProps/core.xml',
            'presentation': 'ppt/presentation.xml',
            'slide1': 'ppt/slides/slide1.xml',
            'slideLayouts': 'ppt/slideLayouts/slideLayout1.xml',
            'slideMasters': 'ppt/slideMasters/slideMaster1.xml',
            'notesSlide': 'ppt/notesSlides/notesSlide1.xml',
            'theme': 'ppt/theme/theme1.xml',
            'presentationRels': 'ppt/_rels/presentation.xml.rels',
            'contentTypes': '[Content_Types].xml'
        },
        'onenote': {
            'onetoc2': 'openNotebookStructure.onetoc2',
            'section': 'sectionFolder'
        }
    }

    if doc_type not in file_paths or location not in file_paths[doc_type]:
        print(f"Unsupported document type or location: {doc_type}, {location}")
        return

    target_file = file_paths[doc_type][location]

    # Read the payload
    if is_file:
        with open(payload, 'r') as file:
            payload_content = file.read()
    else:
        payload_content = payload

    # Unzip the document
    with zipfile.ZipFile(doc_path, 'r') as zip_ref:
        zip_ref.extractall('unzipped_doc')

    # Inject the hidden prompt
    content_path = os.path.join('unzipped_doc', target_file)
    with open(content_path, 'r') as file:
        content = file.read()
    
    # Insert the payload at the specified location
    injection_point = '</Relationships>' if 'rels' in location else '</Properties>' if 'docProps' in location else '</w:document>' if 'document' in location else '</workbook>' if 'workbook' in location else '</presentation>'
    payload_xml = f'<Relationship Id="rIdHidden" Type="http://schemas.microsoft.com/office/2006/relationships/customXml" Target="{payload_content}"/>' if 'rels' in location else f'<property name="hiddenPrompt" fmtid="{{D5CDD505-2E9C-101B-9397-08002B2CF9AE}}" pid="2"><vt:lpwstr>{payload_content}</vt:lpwstr></property>' if 'docProps' in location else f'<customXml><hiddenPrompt>{payload_content}</hiddenPrompt></customXml>'

    content = content.replace(injection_point, f'{payload_xml}{injection_point}')
    
    # Write the updated content back
    with open(content_path, 'w') as file:
        file.write(content)
    
    # Zip the document back up
    with zipfile.ZipFile(f'modified_{os.path.basename(doc_path)}', 'w') as zip_ref:
        for folder_name, subfolders, filenames in os.walk('unzipped_doc'):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'unzipped_doc'))
    
    print(f"Modified document saved as: modified_{os.path.basename(doc_path)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject hidden prompts into Microsoft 365 documents")
    parser.add_argument('doc_type', choices=['word', 'excel', 'powerpoint', 'onenote'], help="Type of the document")
    parser.add_argument('location', choices=['rels', 'docProps', 'document', 'fontTable', 'settings', 'styles', 'theme', 'webSettings', 'docRels', 'contentTypes', 'workbook', 'sharedStrings', 'sheet1', 'workbookRels', 'presentation', 'slide1', 'slideLayouts', 'slideMasters', 'notesSlide', 'presentationRels', 'onetoc2', 'section'], help="Location within the document to inject the payload")
    parser.add_argument('payload', help="Payload to be injected (text or file path)")
    parser.add_argument('--file', action='store_true', help="Indicate if the payload is a file path")

    args = parser.parse_args()
    doc_path = 'path/to/your/document'  # Update this to the path of the document you want to modify
    inject_hidden_prompt(doc_path, args.doc_type, args.location, args.payload, args.file)