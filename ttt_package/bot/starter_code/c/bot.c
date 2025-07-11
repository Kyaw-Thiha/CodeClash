/* starter_bot.c
 * Code Clash Tic Tac Toe Bot Challenge — C Starter Bot
 *
 * Welcome to the Code Clash Tic Tac Toe Bot Competition! This is your starter
 * template. Modify any part of this file to implement your own strategy.
 *
 * == Building ==
 * gcc -std=c11 -O2 -o starter_bot starter_bot.c cJSON.c
 *
 * == Usage ==
 * ./starter_bot /path/to/state.json
 *
 * For rules, move format, and submission details see design_doc.md.
 */

#include "cJSON.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 10 /* Board is 10×10 */

// Parse state.json into a cJSON structure
cJSON *load_state(const char *path) {
  FILE *f = fopen(path, "rb");
  if (!f) {
    perror("fopen");
    exit(1);
  }
  fseek(f, 0, SEEK_END);
  long len = ftell(f);
  fseek(f, 0, SEEK_SET);
  char *data = malloc(len + 1);
  fread(data, 1, len, f);
  data[len] = 0;
  fclose(f);

  cJSON *state = cJSON_Parse(data);
  free(data);
  if (!state) {
    fprintf(stderr, "ERROR: Invalid JSON\n");
    exit(1);
  }
  return state;
}

// Collect all empty cells
void get_valid_moves(cJSON *board, cJSON **out_array) {
  *out_array = cJSON_CreateArray();
  for (int i = 0; i < SIZE; i++) {
    cJSON *row = cJSON_GetArrayItem(board, i);
    for (int j = 0; j < SIZE; j++) {
      const char *cell = cJSON_GetArrayItem(row, j)->valuestring;
      if (cell[0] == 0) {
        cJSON *mv = cJSON_CreateIntArray((int[]){i, j}, 2);
        cJSON_AddItemToArray(*out_array, mv);
      }
    }
  }
}

// TODO: Replace this stub with your move logic
void choose_move(cJSON *valid_moves, int *out_row, int *out_col) {
  int count = cJSON_GetArraySize(valid_moves);
  if (count == 0) {
    fprintf(stderr, "ERROR: No valid moves\n");
    exit(1);
  }
  // stub: pick the first move
  cJSON *mv = cJSON_GetArrayItem(valid_moves, 0);
  *out_row = mv->child->valueint;
  *out_col = mv->child->next->valueint;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s /path/to/state.json\n", argv[0]);
    return 1;
  }
  cJSON *state = load_state(argv[1]);
  cJSON *board = cJSON_GetObjectItem(state, "board");

  cJSON *valid_moves;
  get_valid_moves(board, &valid_moves);

  int row, col;
  choose_move(valid_moves, &row, &col);

  // output
  printf("[%d, %d]\n", row, col);

  cJSON_Delete(valid_moves);
  cJSON_Delete(state);
  return 0;
}
