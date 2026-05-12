package baseline

import "fmt"

// ProcessOrders processes a slice of orders and returns results for pending orders with valid amounts and users.
func ProcessOrders(orders []Order) ([]Result, error) {
	// Iterate over each order to check its status and validity
	var results []Result
	for _, o := range orders {
		// Only process orders that are in "pending" status
		if o.Status != "pending" {
			continue
		}
		// Skip orders with zero or negative amounts
		if o.Amount <= 0 {
			continue
		}
		// UserID must be set; otherwise return an error
		if o.UserID == "" {
			return nil, fmt.Errorf("order %s missing user", o.ID)
		}
		// Append a successful result for this order
		results = append(results, Result{ID: o.ID, Processed: true})
	}
	return results, nil
}

// Order represents a customer order with an ID, user, status, and amount.
type Order struct {
	ID     string
	UserID string
	Status string
	Amount float64
}

// Result holds the outcome of processing a single order.
type Result struct {
	ID        string
	Processed bool
}
