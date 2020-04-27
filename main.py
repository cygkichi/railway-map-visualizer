"""
This modules is xxx
"""
import sys
import yaml
import logging
import argparse

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="""Run a Station Wiki Scraper""")
    parser.add_argument('-c', '--config', type=str, default='./config.yaml')
    args = parser.parse_args()
    return args

def read_config(yamlfile):
    """Read the config yamlfile.
    memo error: yaml not found.
    memo error: cannot read the yaml.
    """
    try:
        logging.info('read yaml:'+yamlfile)
        with open(yamlfile, 'r') as y:
            confdic = yaml.load(y)
        logging.debug('dict of config is '+str(confdic))
        return confdic
    except FileNotFoundError:
        logging.error('File Not Found:'+yamlfile)
        sys.exit(1)


def main(debug_lebel=logging.DEBUG):
    """Run the Scraper."""
    logging.basicConfig(level=debug_lebel)
    logging.info('Start Scraper.')
    args    = parse_arguments()
    confdic = read_config(args.config)


        
if __name__ == '__main__':
    main()
