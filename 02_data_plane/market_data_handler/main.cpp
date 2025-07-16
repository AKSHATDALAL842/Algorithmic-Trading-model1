#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

// Represents a single market data tick
struct MarketDataTick {
    std::string timestamp;
    std::string symbol;
    double bid;
    double ask;
};

// Reads market data from the CSV file
std::vector<MarketDataTick> read_market_data(const std::string& file_path) {
    std::vector<MarketDataTick> ticks;
    std::ifstream file(file_path);
    std::string line;

    // Skip header
    std::getline(file, line);

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string item;
        MarketDataTick tick;

        std::getline(ss, item, ',');
        tick.timestamp = item;
        std::getline(ss, item, ',');
        tick.symbol = item;
        std::getline(ss, item, ',');
        tick.bid = std::stod(item);
        std::getline(ss, item, ',');
        tick.ask = std::stod(item);

        ticks.push_back(tick);
    }
    return ticks;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <path_to_market_data.csv>" << std::endl;
        return 1;
    }

    std::string file_path = argv[1];
    auto ticks = read_market_data(file_path);

    std::cout << "MarketDataHandler: Read " << ticks.size() << " ticks from " << file_path << std::endl;

    // In a real system, this is where you would push ticks into a ring buffer
    // for the book builder to consume.
    for (const auto& tick : ticks) {
        // Simulate processing
    }

    std::cout << "MarketDataHandler: Finished processing all ticks." << std::endl;

    return 0;
}
