// wordle_logic.cpp
#include <string>
#include <vector>
#include <cstring>

extern "C" {

// Function to compare the guessed word with the target word
void evaluate_guess(const char* target_word, const char* guessed_word, char* feedback) {
    std::string target = target_word;
    std::string guess = guessed_word;
    std::vector<char> result(guess.size(), '0'); // Initialize feedback: '0' for gray

    // First pass: Check for correct positions (green)
    for (size_t i = 0; i < guess.size(); i++) {
        if (guess[i] == target[i]) {
            result[i] = '2'; // '2' for green
            target[i] = '*'; // Mark as used
        }
    }

    // Second pass: Check for misplaced letters (yellow)
    for (size_t i = 0; i < guess.size(); i++) {
        if (result[i] == '0') { // Not already green
            size_t pos = target.find(guess[i]);
            if (pos != std::string::npos) {
                result[i] = '1'; // '1' for yellow
                target[pos] = '*'; // Mark as used
            }
        }
    }

    // Copy the feedback to the output array
    std::memcpy(feedback, result.data(), result.size());
}
}
