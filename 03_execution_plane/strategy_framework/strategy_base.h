// Copyright (c) 2025 [Your Firm Name]. All rights reserved.
//
// StrategyBase: An abstract base class for all trading strategies.

#pragma once

// Forward declaration for the order book and order manager
class OrderBook;
class OrderManager;

class StrategyBase {
public:
    StrategyBase(OrderManager* order_manager) : order_manager_(order_manager) {}
    virtual ~StrategyBase() = default;

    // This is the main entry point for the strategy.
    // It will be called by the framework whenever there is a new market data event.
    virtual void OnMarketData(const OrderBook& order_book) = 0;

protected:
    // Strategies will use the order manager to send, cancel, and modify orders.
    OrderManager* order_manager_;
};
