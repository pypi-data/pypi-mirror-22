#!/usr/bin/env python

'''
script.py: part of singularity command line tool
Runtime executable, "shub"

The MIT License (MIT)

Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from glob import glob
import singularity
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(
    description="Singularity Hub command line tool")

    # Single image, must be string
    parser.add_argument("--image", dest='image', 
                        help="full path to singularity image (for use with --package and --tree)", 
                        type=str, default=None)

    parser.add_argument("--version", dest='version', 
                        help="show software version", 
                        default=False, action='store_true')

    # Two images, for similarity function
    parser.add_argument("--images", dest='images', 
                        help="images, separated by commas (for use with --simtree and --subtract", 
                        type=str, default=None)

    # Does the user want to have verbose logging?
    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    # Output folder, if needed
    parser.add_argument("--outfolder", dest='outfolder', 
                        help="full path to folder for output, stays in tmp (or pwd) if not specified", 
                        type=str, default=None)

    # Does the user want to package an image?
    parser.add_argument('--package', dest="package", 
                        help="package a singularity container for singularity hub", 
                        default=False, action='store_true')

    # Does the user want to package an image?
    parser.add_argument('--include-image', dest="include_image", 
                        help="include image file in the package", 
                        default=False, action='store_true')

    # Does the user want to estimate the os?
    parser.add_argument('--os', dest="os", 
                        help="estimate the operating system of your container.", 
                        default=False, action='store_true')

    # Does the user want to estimate the os?
    parser.add_argument('--oscalc', dest="oscalc", 
                        help="calculate similarity score for your container vs. docker library OS.", 
                        default=False, action='store_true')

    # Does the user want to estimate the os?
    parser.add_argument('--osplot', dest="osplot", 
                        help="plot similarity scores for your container vs. docker library OS.", 
                        default=False, action='store_true')

    # Does the user want to get tags for an image?
    parser.add_argument('--tags', dest="tags", 
                        help="retrieve list of software tags for an image, itself minus it's base", 
                        default=False, action='store_true')

    # View the guts of a Singularity image
    parser.add_argument('--tree', dest='tree', 
                        help="view the guts of an singularity image (use --image)", 
                        default=False, action='store_true')

    # Compare two images (a similarity tree)
    parser.add_argument('--simtree', dest='simtree', 
                        help="view common guts between two images (use --images)", 
                        default=False, action='store_true')

    # Compare two images (a similarity tree)
    parser.add_argument('--subtract', dest='subtract', 
                        help="subtract one container image from the second to make a difference tree (use --images first,subtract)", 
                        default=False, action='store_true')

    # Compare two images (get numerical comparison)
    parser.add_argument('--simcalc', dest='simcalc', 
                        help="calculate similarity (number) between images based on file contents.", 
                        default=False, action='store_true')

    # Size, if needed
    parser.add_argument("--size", dest='size', 
                        help="If using Docker or shub image, you can change size (default is 1024)", 
                        type=int, default=1024)

    return parser


def main():

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # Not running in Singularity Hub environment
    os.environ['SINGULARITY_HUB'] = "False"

    # if environment logging variable not set, make silent
    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "CRITICAL"

    if args.version is True:
        print(singularity.__version__)
        sys.exit(0)

    # Initialize the message bot, with level above
    from singularity.logman import bot
    from singularity.utils import check_install
    from singularity.cli import get_image

    # Output folder will be pwd if not specified
    if args.outfolder is None:
        output_folder = os.getcwd()
    else:
        output_folder = args.outfolder

    # We can only continue if singularity is installed
    if check_install() is True:

       # If we are given an image, ensure full path
       if args.image is not None:

           image,existed = get_image(args.image,
                                     return_existed=True,
                                     size=args.size)

           if image is None:
               bot.logger.error("Cannot find image. Exiting.")
               sys.exit(1)

           # the user wants to make a tree
           if args.tree is True:
               from singularity.app import make_tree
               make_tree(image)
               clean_up(image,existed)

           # The user wants to estimate the os
           elif args.os is True:
               from singularity.analysis.classify import estimate_os
               estimated_os = estimate_os(container=image)
               print(estimated_os)

           # The user wants to get a list of all os
           elif args.oscalc is True:
               from singularity.analysis.classify import estimate_os
               estimated_os = estimate_os(container=image,return_top=False)
               print(estimated_os["SCORE"].to_dict())

           # The user wants to get a list of tags
           elif args.tags is True:
               from singularity.analysis.classify import get_tags
               tags = get_tags(container=image)
               print(tags)

           # The user wants to plot image vs. the docker os
           elif args.osplot is True:
               from singularity.app import plot_os_sims
               plot_os_sims(image)
               clean_up(image,existed)

           # The user wants to package the image
           elif args.package is True:
               from singularity.package import package
               remove_image = not args.include_image
               package(image_path=image,
                       output_folder=output_folder,
                       runscript=True,
                       software=True,
                       remove_image=remove_image)
           else:
               print("Not sure what to do?")
               parser.print_help()

       # If we are given two image, we probably want a similar tree
       elif args.images is not None:

           image1,image2 = args.images.split(',')
           bot.logger.debug("Image1: %s",image1)
           bot.logger.debug("Image2: %s",image2)
           image1,existed1 = get_image(image1,
                                       return_existed=True,
                                       size=args.size)
           image2,existed2 = get_image(image2,
                                       return_existed=True,
                                       size=args.size)

           if image1 is None or image2 is None:
               bot.logger.error("Cannot find image. Exiting.")
               sys.exit(1)

           # the user wants to make a similarity tree
           if args.simtree is True:
               from singularity.app import make_sim_tree
               make_sim_tree(image1,image2)

           # the user wants to make a difference tree
           if args.subtract is True:
               from singularity.app import make_diff_tree
               make_diff_tree(image1,image2)

           if args.simcalc is True:
               from singularity.analysis.compare import calculate_similarity
               score = calculate_similarity(image1,image2,by="files.txt")
               print(score["files.txt"])

           clean_up(image1,existed1)
           clean_up(image2,existed2)
    
       else:
          print("Please specify one or more containers with --image(s)")


def clean_up(image,existed):
    '''clean up will remove an image file if existed is False (meaning it was
    created as temporary for the script
    '''
    from singularity.logman import bot
    if existed == False:
        if os.path.exists(image):
            bot.logger.info("%s created was temporary, removing",image)
            os.remove(image)


if __name__ == '__main__':
    main()
