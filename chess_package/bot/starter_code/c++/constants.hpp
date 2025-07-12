#pragma once

#include <map>
#include <string>
#include <utility>
#include <nlohmann/json.hpp>

// Constants for the Code Clash Special Chess Game

// Piece types for setup phase (maps single-letter identifiers to board UI column)
const std::map<std::string, std::pair<int, int>> PIECE_TYPES_SETUP = {
    {"K", {0, 0}},  // King
    {"Q", {0, 1}},  // Queen
    {"R", {0, 2}},  // Rook
    {"B", {0, 3}},  // Bishop
    {"P", {0, 4}},  // Pawn
};

// Fog placeholder used when a tile is hidden
const nlohmann::json FOG_PIECE = {
    {"color", "fog"},
    {"type", "F"}
};