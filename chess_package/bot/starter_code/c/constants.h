/*
 * Code Clash Chess Challenge — C Constants
 */

#ifndef CONSTANTS_H
#define CONSTANTS_H

#define BOARD_SIZE 5

// Piece types at setup phase: keys & their "column index"
static const char *PIECE_TYPES_SETUP_KEYS[] = {"K","Q","R","B","P"};
static const int   PIECE_TYPES_SETUP_VALUES[][2] = {
    {0,0},  // K
    {0,1},  // Q
    {0,2},  // R
    {0,3},  // B
    {0,4},  // P
};
#define PIECE_TYPES_SETUP_COUNT 5

// Fog piece for hidden tiles in state.json (if you ever need it)
#define FOG_COLOR "fog"
#define FOG_TYPE  "F"

#endif // CONSTANTS_H