package with_rule

import "fmt"

type Order struct {
	ID, UserID, Status string
	Amount             float64
}

type Result struct {
	ID        string
	Processed bool
}

func ProcessOrders(orders []Order) ([]Result, error) {
	var results []Result
	for _, o := range orders {
		if o.Status != "pending" || o.Amount <= 0 {
			continue
		}
		if o.UserID == "" {
			return nil, fmt.Errorf("order %s missing user", o.ID)
		}
		results = append(results, Result{ID: o.ID, Processed: true})
	}
	return results, nil
}
