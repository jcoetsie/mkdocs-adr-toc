import os
import re
import logging
import shutil
from tempfile import TemporaryDirectory
from mkdocs.plugins import BasePlugin
from mkdocs.utils import log as logger
from mkdocs import config

class ADRTOCPluginConfig(config.base.Config):
    toc_file = config.config_options.Type(str, default='index.md')
    placeholder = config.config_options.Type(str, default='<!-- ADR_SUMMARY_PLACEHOLDER -->')
    adr_path = config.config_options.Type(str, default='decisions')

class ADRTOCPlugin(BasePlugin[ADRTOCPluginConfig]):

    def on_pre_build(self, config):

        # Define the directory containing the ADR records
        decisions_dir = os.path.join(config['docs_dir'], self.config.adr_path)

        # Regular expressions to extract the status, date, title, and deciders
        status_re = re.compile(r'^status:\s*"(.+)"', re.MULTILINE)
        date_re = re.compile(r'^date:\s*"(.+)"', re.MULTILINE)
        title_re = re.compile(r'^#\s+(.+)', re.MULTILINE)
        deciders_re = re.compile(r'^deciders:\s*\[(.+)\]', re.MULTILINE)

        # List to hold the ADR records
        adr_records = []

        # Loop over all files in the decisions directory
        logger.debug(f'Starting to process ADR files in directory: {decisions_dir}')
        for filename in os.listdir(decisions_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(decisions_dir, filename)
                logger.debug(f'Processing file: {filepath}')
                with open(filepath, 'r') as file:
                    content = file.read()
                    status_match = status_re.search(content)
                    date_match = date_re.search(content)
                    title_match = title_re.search(content)
                    deciders_match = deciders_re.search(content)
                    if title_match:
                        decision_number = filename.split('-')[0]
                        title = title_match.group(1)
                        status = status_match.group(1) if status_match else 'Unknown'
                        date = date_match.group(1) if date_match else 'Unknown'
                        deciders = deciders_match.group(1).replace('"', '').strip() if deciders_match else 'Unknown'
                        adr_records.append({
                            'number': decision_number,
                            'title': title,
                            'status': status,
                            'date': date,
                            'deciders': deciders,
                            'filename': filename
                        })
                        logger.debug(f'Added ADR: {title}')
                    else:
                        logger.warning(f'Failed to extract title from file: {filepath}')

        # Sort the ADR records by number
        adr_records.sort(key=lambda x: x['number'])

        # Generate the ADR summary content
        adr_summary_content = '# ADR Summary\n\n'
        adr_summary_content += '| Number | Decision | Status | Last Review Date | Deciders |\n'
        adr_summary_content += '| --- | --- | --- | --- | --- |\n'
        for record in adr_records:
            number_link = f"[{record['number']}]({os.path.join(self.config.adr_path, record['filename'])})"
            title_link = f"[{record['title']}]({os.path.join(self.config.adr_path, record['filename'])})"
            adr_summary_content += f"| {number_link} | {title_link} | {record['status']} | {record['date']} | {record['deciders']} |\n"
            logger.debug(f'Added record to summary: {record["title"]}')

        # Replace the placeholder in the existing file
        existing_file = os.path.join(config['docs_dir'], self.config.adr_path, self.config.toc_file)
        if os.path.exists(existing_file):
            with open(existing_file, 'r') as file:
                content = file.read()
            content = content.replace(self.config.placeholder, adr_summary_content)
            with open(existing_file, 'w') as file:
                file.write(content)
            logger.info(f'Replaced {self.config.placeholder} in {existing_file}')
        else:
            logger.warning(f'Existing file {existing_file} not found')

    def on_page_markdown(self, markdown, page, config, files):
        # Check if the current page is the one specified for the TOC
        if page.file.src_path == self.config.toc_file:
            logger.debug(f'Injecting ADR summary into page: {page.file.src_path}')
            
            # Define the directory containing the ADR records
            decisions_dir = os.path.join(config['docs_dir'], self.config.adr_path)
            logger.debug(f'Decisions directory: {decisions_dir}')

            # Regular expressions to extract the status, date, title, and deciders
            status_re = re.compile(r'^status:\s*"(.+)"', re.MULTILINE)
            date_re = re.compile(r'^date:\s*"(.+)"', re.MULTILINE)
            title_re = re.compile(r'^#\s+(.+)', re.MULTILINE)
            deciders_re = re.compile(r'^deciders:\s*\[(.+)\]', re.MULTILINE)

            # List to hold the ADR records
            adr_records = []

            # Loop over all files in the decisions directory
            logger.debug(f'Starting to process ADR files in directory: {decisions_dir}')
            for filename in os.listdir(decisions_dir):
                if filename.endswith('.md'):
                    filepath = os.path.join(decisions_dir, filename)
                    logger.debug(f'Processing file: {filepath}')
                    with open(filepath, 'r') as file:
                        content = file.read()
                        status_match = status_re.search(content)
                        date_match = date_re.search(content)
                        title_match = title_re.search(content)
                        deciders_match = deciders_re.search(content)
                        if title_match:
                            decision_number = filename.split('-')[0]
                            title = title_match.group(1)
                            status = status_match.group(1) if status_match else 'Unknown'
                            date = date_match.group(1) if date_match else 'Unknown'
                            deciders = deciders_match.group(1).replace('"', '').strip() if deciders_match else 'Unknown'
                            adr_records.append({
                                'number': decision_number,
                                'title': title,
                                'status': status,
                                'date': date,
                                'deciders': deciders,
                                'filename': filename
                            })
                            logger.debug(f'Added ADR: {title}')
                        else:
                            logger.warning(f'Failed to extract title from file: {filepath}')

            # Sort the ADR records by number
            adr_records.sort(key=lambda x: x['number'])

            # Generate the ADR summary content
            adr_summary_content = '# ADR Summary\n\n'
            adr_summary_content += '| Number | Decision | Status | Last Review Date | Deciders |\n'
            adr_summary_content += '| --- | --- | --- | --- | --- |\n'
            for record in adr_records:
                number_link = f"[{record['number']}]({os.path.join(self.config.adr_path, record['filename'])})"
                title_link = f"[{record['title']}]({os.path.join(self.config.adr_path, record['filename'])})"
                adr_summary_content += f"| {number_link} | {title_link} | {record['status']} | {record['date']} | {record['deciders']} |\n"
                logger.debug(f'Added record to summary: {record["title"]}')

            # Replace the placeholder in the existing file
            existing_file = os.path.join(config['docs_dir'], self.config.adr_path, self.config.toc_file)
            if os.path.exists(existing_file):
                with open(existing_file, 'r') as file:
                    content = file.read()
                content = content.replace(self.config.placeholder, adr_summary_content)
                with open(existing_file, 'w') as file:
                    file.write(content)
                logger.info(f'Replaced {self.config.placeholder} in {existing_file}')
            else:
                logger.warning(f'Existing file {existing_file} not found')
