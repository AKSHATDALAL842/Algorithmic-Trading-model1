#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <deque>
#include <numeric>
#include <cmath>
#include <map>

// --- Data Structures ---
struct MarketDataTick {
    std::string timestamp;
    std::string symbol;
    double bid;
    double ask;
};

class Portfolio {
public:
    double cash = 100000.0;
    std::map<std::string, int> positions;

    void execute_trade(const std::string& symbol, const std::string& side, double price, int quantity) {
        double cost = price * quantity;
        if (side == "BUY") {
            cash -= cost;
            positions[symbol] += quantity;
        } else if (side == "SELL") {
            cash += cost;
            positions[symbol] -= quantity;
        }
    }
};

class PairTradingStrategy {
public:
    PairTradingStrategy(Portfolio& portfolio) : portfolio(portfolio) {}

    void on_market_data(const MarketDataTick& data) {
        double mid_price = (data.bid + data.ask) / 2.0;

        if (data.symbol == "SYMA") {
            prices_a.push_back(mid_price);
        } else if (data.symbol == "SYMB") {
            prices_b.push_back(mid_price);
        }

        if (!prices_a.empty() && !prices_b.empty()) {
            double spread = prices_a.back() - prices_b.back();
            spread_history.push_back(spread);
            if (spread_history.size() > window) {
                spread_history.pop_front();
            }

            if (spread_history.size() == window) {
                double mean_spread = std::accumulate(spread_history.begin(), spread_history.end(), 0.0) / window;
                double sq_sum = std::inner_product(spread_history.begin(), spread_history.end(), spread_history.begin(), 0.0);
                double std_spread = std::sqrt(sq_sum / window - mean_spread * mean_spread);
                double z_score = (spread - mean_spread) / std_spread;

                if (z_score > threshold && portfolio.positions["SYMA"] == 0) {
                    portfolio.execute_trade("SYMA", "SELL", data.bid, 100);
                    portfolio.execute_trade("SYMB", "BUY", data.ask, 100);
                } else if (z_score < -threshold && portfolio.positions["SYMA"] == 0) {
                    portfolio.execute_trade("SYMA", "BUY", data.ask, 100);
                    portfolio.execute_trade("SYMB", "SELL", data.bid, 100);
                } else if (std::abs(z_score) < 0.5 && portfolio.positions["SYMA"] != 0) {
                    portfolio.execute_trade("SYMA", "BUY", data.ask, portfolio.positions["SYMA"]);
                    portfolio.execute_trade("SYMB", "SELL", data.bid, portfolio.positions["SYMB"]);
                }
            }
        }
    }

private:
    Portfolio& portfolio;
    std::deque<double> prices_a, prices_b, spread_history;
    const int window = 20;
    const double threshold = 2.0;
};

// --- Main Application ---
std::vector<MarketDataTick> read_market_data(const std::string& file_path) {
    std::vector<MarketDataTick> ticks;
    std::ifstream file(file_path);
    std::string line;
    std::getline(file, line); // Skip header
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string item;
        MarketDataTick tick;
        std::getline(ss, item, ','); tick.timestamp = item;
        std::getline(ss, item, ','); tick.symbol = item;
        std::getline(ss, item, ','); tick.bid = std::stod(item);
        std::getline(ss, item, ','); tick.ask = std::stod(item);
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

    Portfolio portfolio;
    PairTradingStrategy strategy(portfolio);

    std::cout << "Running C++ Live Simulation..." << std::endl;
    for (const auto& tick : ticks) {
        strategy.on_market_data(tick);
    }

    std::cout << "Simulation Complete." << std::endl;
    std::cout << "--- C++ Simulation Results ---" << std::endl;
    std::cout.precision(2);
    std::cout << std::fixed;
    std::cout << "Final Cash: $" << portfolio.cash << std::endl;
    double pnl = portfolio.cash - 100000.0;
    std::cout << "Net Profit/Loss: $" << pnl << std::endl;

    return 0;
}
