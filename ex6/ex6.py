#!/usr/bin/env python3
#############################################################
# FILE :        ex6.py
# WRITER :      Raz Karl , razkarl , 311143127
# EXERCISE :    intro2cs ex6 2016-2017
# DESCRIPTION:  Create a mosaic of a picture from a set of
#               of images.
#############################################################
import argparse
import math
import time
from mosaic import *

# Command line arguments defaults
PROG_DECRIPTION     = 'Create a mosaic of a picture from a set of of images.'
DEFAULT_IMAGE_SRC   = 'im1.jpg'
DEFAULT_IMAGES_DIR  = 'images'
DEFAULT_OUTPUT_NAME = 'out.jpg'
DEFAULT_TILE_SIZE   = '40'
DEFAULT_NUM_CANDS   = '100'
DEFAULT_ARGS        =  [DEFAULT_IMAGE_SRC,
                        DEFAULT_IMAGES_DIR,
                        DEFAULT_OUTPUT_NAME,
                        DEFAULT_TILE_SIZE,
                        DEFAULT_NUM_CANDS]

# Pixel tuple constants
EMPTY_PIXEL = (0,0,0)
RED   = 0
GREEN = 1
BLUE  = 2

# Size tuple constants
HEIGHT    = 0
WIDTH     = 1


def num_rows(image):
    """
    @brief      returns the number of rows in an image.

    @param      image   list of lists of tuples: 
                        [rows][columns](R,G,B) of image pixels.

    @return     int: number of rows in the image.
    """
    return len(image)


def num_cols(image):
    """
    @brief      returns the number of columns in an image.

    @param      image   list of lists of tuples: 
                        [rows][columns](R,G,B) of image pixels.

    @return     int: number of columns in the image.
    """
    return len(image[0])  # image[0] = first row, therefore it's length is the 
                          # number of cols.

def compare_pixel(pixel1, pixel2):
    """
    @brief      Calculate differences between 2 pixels.
    
    @param      pixel1  tuple: (R,G,B) values for pixel 1.
    @param      pixel2  tuple: (R,G,B) values for pixel 2.
    
    @return     int: |R1-R2| + |G1-G2| + |B1-B2|
    """
    return  abs(pixel1[RED]   - pixel2[RED])    + \
            abs(pixel1[GREEN] - pixel2[GREEN])  + \
            abs(pixel1[BLUE]  - pixel2[BLUE])


def compare(image1, image2):
    """
    @brief      Calculate overall pixel difference between 2 images.
    
    @param      image1  list of lists of tuples: 
                        [rows][columns](R,G,B) of image1 pixels.
    @param      image2  list of lists of tuples: 
                        [rows][columns](R,G,B) of image2 pixels.

    @notice     if the images are not of the same size, compares the overlapping
                part.
    @notice     all rows in an image must be of the same length, same applies 
                for columns.
    
    @return     int: sum of pixel differences as returned from compare_pixel.
    """
    # Calculate overlapping part and crop if needed    
    overlap_rows = min(num_rows(image1), num_rows(image2))
    overlap_cols = min(num_cols(image1), num_cols(image2))
    
    # Sum differences for all overlapping pixels
    total_dif = 0
    for row in range(overlap_rows):
       for col in range(overlap_cols):
            total_dif += compare_pixel( image1[row][col],
                                        image2[row][col])
    return total_dif


def get_piece(image, upper_left, size):
    """
    @brief      Gets a piece of given size from an image cropped from the upper
                left corner.
    
    @param      image       list of lists of tuples:  
                            [rows][columns](R,G,B) of image pixels.
    @param      upper_left  (row, col): location of the pixel in the image which
                            will be the upper left pixel of the piece.
    @param      size        tuple: (heigt,width) of the piece.
    
    @notice     if the piece exceeds the image borders it will be cropped.

    @return     list of lists of tuples:
                [rows][columns](R,G,B) of piece pixels.
    """
    # Get piece location and crop any negative parts
    piece_y = max(upper_left[HEIGHT], 0)
    piece_x = max(upper_left[WIDTH],  0)

    # Calculate overlapping part and crop if needed
    overlap_rows = min(size[HEIGHT],  num_rows(image)-piece_y)
    overlap_cols = min(size[WIDTH],   num_cols(image)-piece_x)

    # Get da piece madafaka
    piece = [[image[piece_y + row][piece_x + col]   \
             for col in range(overlap_cols)]        \
            for row in range(overlap_rows)]
    return piece


def set_piece(image, upper_left, piece):
    """
    @brief      Places a piece of given size inside an image cropped to not 
                exceed image borders.
    
    @param      image       list of lists of tuples:  
                            [rows][columns](R,G,B) of image pixels.
    @param      upper_left  (row, col): location of the pixel in the image which
                            is the upper left pixel of the piece.
    @param      piece       list of lists of tuples:  
                            [rows][columns](R,G,B) of piece pixels.

    @notice     if the piece exceeds the image borders it will be cropped.
    """
    # Get piece location and crop any negative parts
    piece_y = max(upper_left[HEIGHT], 0)
    piece_x = max(upper_left[WIDTH],  0)

    # Calculate overlapping area and crop if needed
    overlap_rows = min(num_rows(piece), num_rows(image)-piece_y)
    overlap_cols = min(num_cols(piece), num_cols(image)-piece_x)

    # Set da piece madafaka
    for row in range(overlap_rows):
        for col in range(overlap_cols):
            image[row + piece_y][col + piece_x] = piece[row][col]
    

def average(image):
    """
    @brief      Calculates average RGB value from all the pixels in the image.
    
    @param      list of lists of tuples:  
                [rows][columns](R,G,B) of image pixels.
    
    @return     tuple: (float: average RED, 
                        float: average GREEN, 
                        float: average BLUE)
    """
    total_RED, total_GREEN, total_BLUE = 0, 0, 0
    pixels_examined = 0

    # Accumulate all pixels
    for row in range(num_rows(image)):
        for col in range(num_cols(image)):
            pixel = image[row][col]
            total_RED   += pixel[RED]
            total_GREEN += pixel[GREEN]
            total_BLUE  += pixel[BLUE]
            pixels_examined += 1

    # Calculate average values
    average = (total_RED   / pixels_examined,
               total_GREEN / pixels_examined,
               total_BLUE  / pixels_examined)

    return average


def preprocess_tiles(tiles):
    """
    @brief      Returns a list of the tiles' color averages.
    
    @param      tiles  list of tiles:
                [tile_index][rows][columns](R,G,B) of tile pixels.
    
    @return     list of tuples: [tile_index](average RED,
                                             average GREEN,
                                             average BLUE)
    """
    return [average(tile) for tile in tiles]


def get_best_tiles(objective, tiles, averages, num_candidates):
    """
    @brief      Gets the best tiles for building the objective mosaic.
    
    @param      objective       list of lists of tuples:  
                                [rows][columns](R,G,B) of objective image 
                                pixels. 
    @param      tiles           list of tiles:
                                [tile_index][rows][columns](R,G,B) of tile 
                                pixels.
    @param      averages        list of average pixel colors per tile.
    @param      num_candidates  The number of candidates to return.
    
    @return     The best num_candidates tiles for the objective mosaic.
    """
    # Calculate objective color average to compare with tile averages
    objctv_avg = average(objective)

    # List average differences between tiles and objective
    avg_difs = [compare_pixel(objctv_avg, tile_avg) for tile_avg in averages]

    # Sort tiles by average differences from objective
    sorted_tiles = [tile for (average, tile) in sorted(zip(avg_difs, tiles))]

    # Return best tiles (up to num_candidates)
    return sorted_tiles[:num_candidates]


def choose_tile(piece, tiles):
    """
    @brief      Returns the best tile to replace the given piece.
    
    @param      piece  list of lists of tuples:  
                       [rows][columns](R,G,B) of piece pixels.
    @param      tiles  list of tiles:
                       [tile_index][rows][columns](R,G,B) of tile pixels.
    
    @return     tile: [rows][columns](R,G,B) of the tile that best matches the 
                given piece.
    """
    # Build list of differences between each tile and the piece
    tile_difs = [compare(tile, piece) for tile in tiles]

    # Choose the tile with the minimal difference
    min_dif, best_tile = min((dif, tile) for dif, tile in zip(tile_difs, tiles)) 

    return best_tile


def make_mosaic(image, tiles, num_candidates):
    """
    @brief      Makes a photomosaic of an image from a set of tiles.
    
    @param      image           The mosaic image.
                                list of lists of tuples:  
                                [rows][columns](R,G,B) of image pixels.
    @param      tiles           List of tiles to build the mosaic from.
                                [tile_index][rows][columns](R,G,B) of tile 
                                pixels.
    @param      num_candidates  The number of different tiles to use for the 
                                mosaic.
    
    @notice     Assuming all tiles are of the same size.

    @return     A mosaic image: list of lists of tuples:  
                                [rows][columns](R,G,B) of mosaic pixels.
    """
    # Calculate number of tile rows and columns in the mosaic
    generic_tile = tiles[0] # All tiles are of the same size, so tiles[0] is 
                            # just a representative.
    image_size    = (num_rows(image),         num_cols(image))
    tile_size     = (num_rows(generic_tile),  num_cols(generic_tile))
    rows_of_tiles = math.ceil(image_size[HEIGHT] / tile_size[HEIGHT])
    cols_of_tiles = math.ceil(image_size[WIDTH]  / tile_size[WIDTH])

    # Calculate tiles' average colors for fast comparisons later
    tiles_averages = preprocess_tiles(tiles)

    # Init an empty mosaic to generate from the picture
    mosaic = [[EMPTY_PIXEL 
               for col in range(image_size[WIDTH])] 
              for row in range(image_size[HEIGHT])]

    # For every piece of the image place a similar tile in the mosaic
    for tile_row in range(rows_of_tiles):
        for tile_col in range(cols_of_tiles):
            
            # Calculate current tile position
            tile_position = (tile_size[HEIGHT] * tile_row, 
                             tile_size[WIDTH]  * tile_col)

            # Grab an image piece to match with a tile
            image_piece = get_piece(image, 
                                    tile_position,
                                    tile_size)

            # Filter tiles to good candidates
            best_tiles = get_best_tiles(image_piece, tiles, 
                                        tiles_averages, 
                                        num_candidates)

            # Carefully choose the closest match
            chosen_tile = choose_tile(image_piece, best_tiles)

            # Place the matching tile in the mosaic
            set_piece(mosaic, tile_position, chosen_tile)

    return mosaic


def parse(args=DEFAULT_ARGS):
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=PROG_DECRIPTION)
    parser.add_argument('image_source', type=str, 
                        help="path to a .jpg picture - the mosaic objective.")
    parser.add_argument('images_dir', type=str, 
                        help="path to directory containing only .jpg images - \
                        the mosaic tiles.")
    parser.add_argument('output_name', type=str, 
                        help="path of output file.")
    parser.add_argument('tile_height', type=int, 
                        help="size in pixels of the mosaic tiles.")
    parser.add_argument('num_candidates', type=int, 
                        help="adjusts accuracy - larger numbers lead \
                        to slower runs but possibly more accurate results.")
    return parser.parse_args()


def main():
    args = parse()
    tiles = build_tile_base(args.images_dir, args.tile_height)
    image = load_image(args.image_source)
    mosaic = make_mosaic(image, tiles, args.num_candidates)
    save(mosaic, args.output_name)
    

if __name__ == '__main__':
    main()