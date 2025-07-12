/* bot.c
 * Code Clash Chess Challenge — C Starter Bot
 *
 * Usage:
 *   gcc -std=c11 bot.c cJSON.c -o bot
 *   ./bot /path/to/state.json
 *
 * Output:
 *   Writes `move.json` in the current directory.
 */

#include <stdio.h>
#include <stdlib.h>
#include "cJSON.h"
#include "constants.h"

// Load the full JSON state from disk
cJSON *load_state(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) {
        fprintf(stderr, "Error: cannot open %s\n", path);
        exit(1);
    }
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    char *data = malloc(len + 1);
    fread(data, 1, len, f);
    data[len] = '\0';
    fclose(f);

    cJSON *state = cJSON_Parse(data);
    free(data);
    if (!state) {
        fprintf(stderr, "Error: invalid JSON in %s\n", path);
        exit(2);
    }
    return state;
}

// Write the bot's chosen move into move.json
void write_move(cJSON *move) {
    FILE *f = fopen("move.json", "w");
    if (!f) {
        fprintf(stderr, "Error: cannot write move.json\n");
        exit(3);
    }
    char *out = cJSON_Print(move);
    fprintf(f, "%s\n", out);
    fclose(f);
    cJSON_free(out);
}

// Called when phase == "setup"
cJSON *setup_phase(cJSON *state) {
    /*
     * TODO: implement your setup logic.
     * state->["setupStep"], ["playerColor"], ["board"], ["blockedTiles"], etc.
     *
     * return a JSON object like:
     * {
     *   "move": { "from": [x,y], "to": [r,c] },
     *   "ability": { "name": NULL, "target": NULL }
     * }
     */
    cJSON *move = cJSON_CreateObject();
    cJSON *mv = cJSON_CreateObject();
    cJSON_AddItemToObject(move, "move", mv);
    cJSON_AddItemToObject(mv, "from", cJSON_CreateNull());
    cJSON_AddItemToObject(mv, "to", cJSON_CreateIntArray((int[]){0,0}, 2));

    cJSON *ab = cJSON_CreateObject();
    cJSON_AddItemToObject(move, "ability", ab);
    cJSON_AddItemToObject(ab, "name", cJSON_CreateNull());
    cJSON_AddItemToObject(ab, "target", cJSON_CreateNull());

    return move;
}

// Called when phase == "play"
cJSON *play_phase(cJSON *state) {
    /*
     * TODO: implement your play logic.
     * state->["phase"], ["board"], ["abilitiesRemaining"], etc.
     *
     * return a JSON object like:
     * {
     *   "move": { "from": [r1,c1], "to": [r2,c2] },
     *   "ability": { "name": NULL, "target": NULL }
     * }
     */
    cJSON *move = cJSON_CreateObject();
    cJSON *mv = cJSON_CreateObject();
    cJSON_AddItemToObject(move, "move", mv);
    cJSON_AddItemToObject(mv, "from", cJSON_CreateIntArray((int[]){0,0}, 2));
    cJSON_AddItemToObject(mv, "to", cJSON_CreateIntArray((int[]){0,1}, 2));

    cJSON *ab = cJSON_CreateObject();
    cJSON_AddItemToObject(move, "ability", ab);
    cJSON_AddItemToObject(ab, "name", cJSON_CreateNull());
    cJSON_AddItemToObject(ab, "target", cJSON_CreateNull());

    return move;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s /path/to/state.json\n", argv[0]);
        return 1;
    }

    cJSON *state = load_state(argv[1]);
    const cJSON *phase = cJSON_GetObjectItemCaseSensitive(state, "phase");
    if (!cJSON_IsString(phase)) {
        fprintf(stderr, "Error: missing phase in state.json\n");
        return 2;
    }

    cJSON *move = NULL;
    if (strcmp(phase->valuestring, "setup") == 0) {
        move = setup_phase(state);
    } else {
        move = play_phase(state);
    }

    write_move(move);

    cJSON_Delete(move);
    cJSON_Delete(state);
    return 0;
}