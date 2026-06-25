package com.menulytics.backend.controller;

import com.menulytics.backend.dto.ApiResponse;
import com.menulytics.backend.dto.RestaurantResponse;
import com.menulytics.backend.model.Restaurant;
import com.menulytics.backend.service.RestaurantService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/restaurants")
@CrossOrigin("*")
public class RestaurantController {

    private final RestaurantService service;

    public RestaurantController(RestaurantService service) {
        this.service = service;
    }

    // GET ALL
    @GetMapping
    public ApiResponse<List<Restaurant>> getAll() {
        return new ApiResponse<>(true, "All restaurants fetched", service.getAllRestaurants());
    }

    // SEARCH SIMPLE
    @GetMapping("/search")
    public ApiResponse<List<Restaurant>> search(@RequestParam String name) {
        return new ApiResponse<>(true, "Search results", service.searchByName(name));
    }

    // TRENDING (DTO RESPONSE)
    @GetMapping("/trending")
        public ApiResponse<List<RestaurantResponse>> trending(
        @RequestParam(defaultValue = "10") int limit
    ) {
    return new ApiResponse<>(
            true,
            "Trending restaurants",
            service.getTrending(limit)
    );
    }
    // CAFES
    @GetMapping("/cafes")
    public ApiResponse<List<Restaurant>> cafes() {
        return new ApiResponse<>(true, "Cafe restaurants", service.getCafes());
    }

    // DATE NIGHT
    @GetMapping("/date-night")
    public ApiResponse<List<Restaurant>> dateNight() {
        return new ApiResponse<>(true, "Date night restaurants", service.getDateNight());
    }

    // AREA
    @GetMapping("/area")
    public ApiResponse<List<Restaurant>> byArea(@RequestParam String name) {
        return new ApiResponse<>(true, "Area results", service.getByArea(name));
    }

    // BUDGET LOW
    @GetMapping("/budget/low")
    public ApiResponse<List<Restaurant>> lowBudget() {
        return new ApiResponse<>(true, "Low budget restaurants", service.getBudgetLow());
    }

    // BUDGET MID
    @GetMapping("/budget/mid")
    public ApiResponse<List<Restaurant>> midBudget() {
        return new ApiResponse<>(true, "Mid budget restaurants", service.getBudgetMid());
    }

    // BUDGET HIGH
    @GetMapping("/budget/high")
    public ApiResponse<List<Restaurant>> highBudget() {
        return new ApiResponse<>(true, "High budget restaurants", service.getBudgetHigh());
    }

    // BEST VALUE
    @GetMapping("/best-value")
    public ApiResponse<List<Restaurant>> bestValue() {
        return new ApiResponse<>(true, "Best value restaurants", service.getBestValue());
    }

    // ADVANCED SEARCH
    @GetMapping("/search/advanced")
    public ApiResponse<List<RestaurantResponse>> searchAdvanced(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String area,
            @RequestParam(required = false) String budget,
            @RequestParam(required = false) String category
    ) {
        return new ApiResponse<>(
                true,
                "Advanced search results",
                service.searchRestaurants(name, area, budget, category)
        );
    }

    @GetMapping("/similar")
public ApiResponse<List<Restaurant>> similar(
        @RequestParam String name
) {
    return new ApiResponse<>(
            true,
            "Similar restaurants fetched",
            service.getSimilarRestaurants(name)
    );
}


@GetMapping("/rating")
public ApiResponse<List<Restaurant>> rating(
        @RequestParam double min
){
    return new ApiResponse<>(
            true,
            "Rating filtered restaurants",
            service.getByRating(min)
    );
}
}