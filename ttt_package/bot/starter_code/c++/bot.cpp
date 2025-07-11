// starter_bot.cpp
/*
 * Code Clash Tic Tac Toe Bot Challenge — C++ Starter Bot
 *
 * Welcome to the Code Clash Tic Tac Toe Bot Competition! This is your starter template.
 * Modify any part of this file to implement your own strategy.
 *
 * == Building ==
 * g++ -std=c++17 -O2 -o starter_bot starter_bot.cpp
 *
 * == Usage ==
 * ./starter_bot /path/to/state.json
 *
 * For rules, move format, and submission details see design_doc.md.
 */

#include <iostream>
#include <fstream>
#include <vector>
#include "json.hpp"

using json = nlohmann::json;

// Return list of empty positions on the board
std::vector<std::pair<int,int>> get_valid_moves(const json& board) {
    std::vector<std::pair<int,int>> moves;
    int n = board.size();
    for(int i=0;i<n;++i){
        for(int j=0;j<(int)board[i].size();++j){
            if(board[i][j].get<std::string>().empty()){
                moves.emplace_back(i,j);
            }
        }
    }
    return moves;
}

// TODO: Replace this stub with your own move logic
std::pair<int,int> choose_move(const json& board, const std::string& player) {
    auto valid = get_valid_moves(board);
    if(valid.empty()) {
        throw std::runtime_error("No valid moves available");
    }
    // stub: always return first
    return valid.front();
}

int main(int argc, char* argv[]){
    if(argc!=2){
        std::cerr<<"Usage: "<<argv[0]<<" /path/to/state.json\n";
        return 1;
    }
    // 1) load state.json
    json state;
    try {
        std::ifstream f(argv[1]);
        f >> state;
    } catch (...) {
        std::cerr<<"ERROR: Failed to read or parse state.json\n";
        return 1;
    }

    // 2) extract
    auto board  = state["board"];
    auto player = state["player"].get<std::string>();

    // 3) choose move
    int row, col;
    try {
        std::tie(row,col) = choose_move(board, player);
    } catch (std::exception& e) {
        std::cerr<<"ERROR: "<<e.what()<<"\n";
        return 1;
    }

    // 4) output JSON array to stdout
    std::cout<<"["<<row<<", "<<col<<"]\n";
    return 0;
}