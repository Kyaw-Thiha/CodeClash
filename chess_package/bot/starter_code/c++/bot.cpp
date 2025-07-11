// === Code Clash: Special Chess Bot (C++) ===
// This is the official empty C++ starter shell for building a bot.
// You may modify anything and everything in this file.
//
// == Building ==
// 1. Make sure you have a C++17 compiler (e.g., g++ >= 7.0).
// 2. Download `json.hpp` from: https://github.com/nlohmann/json (Already provided in this directory)
// 3. Compile using:
//      g++ -std=c++17 bot.cpp -o bot
//
// == Running ==
// ./bot path/to/state.json
//
// == Event Info ==
// Code Clash: Special Chess Variant 2025 — Hosted by C.R.E.A.T.E.

#include <iostream>
#include <fstream>
#include <string>
#include "json.hpp"
#include "constants.hpp"

using json = nlohmann::json;

// Helper: load the game state from a file
json load_state(const std::string& path) {
    std::ifstream file(path);
    if (!file) {
        std::cerr << "Error: Failed to open " << path << std::endl;
        std::exit(1);
    }
    json state;
    file >> state;
    return state;
}

// Helper: write bot's move to move.json
void write_move(const json& move_data) {
    std::ofstream file("move.json");
    if (!file) {
        std::cerr << "Error: Failed to write move.json" << std::endl;
        std::exit(2);
    }
    file << move_data.dump(2);
}

// Placeholder for setup logic (step 1–4)
json setup_phase(const json& state) {
    // TODO: Your code here
    return {
        {"move", {
            {"from", nullptr},
            {"to", {0, 0}} // placeholder
        }},
        {"ability", {
            {"name", nullptr},
            {"target", nullptr}
        }}
    };
}

// Placeholder for play logic
json play_phase(const json& state) {
    // TODO: Your code here
    return {
        {"move", {
            {"from", {0, 0}}, // placeholder
            {"to", {0, 1}}    // placeholder
        }},
        {"ability", {
            {"name", nullptr},
            {"target", nullptr}
        }}
    };
}

// Main bot entrypoint
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./bot path/to/state.json" << std::endl;
        return 1;
    }

    json state;
    try {
        state = load_state(argv[1]);
    } catch (const std::exception& e) {
        std::cerr << "Error: Failed to parse state.json — " << e.what() << std::endl;
        return 1;
    }

    std::string phase = state.value("phase", "");
    json move;

    try {
        if (phase == "setup") {
            move = setup_phase(state);
        } else {
            move = play_phase(state);
        }

        write_move(move);
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error during bot logic: " << e.what() << std::endl;
        return 3;
    }
}