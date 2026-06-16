package com.menulytics.backend.service;

import com.menulytics.backend.dto.RestaurantResponse;
import com.menulytics.backend.model.Restaurant;
import jakarta.annotation.PostConstruct;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class RestaurantService {

    private final List<Restaurant> restaurantList = new ArrayList<>();

    @PostConstruct
    public void init() {
        loadCSV();
        System.out.println("Loaded restaurants: " + restaurantList.size());
    }

    private void loadCSV() {
        try {
            ClassPathResource resource =
                    new ClassPathResource("data/indore_restaurants_features.csv");

            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(resource.getInputStream())
            );

            String line;
            boolean firstLine = true;

            while ((line = reader.readLine()) != null) {

                if (firstLine) {
                    firstLine = false;
                    continue;
                }

                try {
                    String[] data = line.split(",", -1);

                    if (data.length < 5) continue;

                    Restaurant r = new Restaurant();

                    r.setRestaurantName(data[0].trim());
                    r.setRating(parseDoubleSafe(data[1]));
                    r.setTotalReviews(parseIntSafe(data[2]));
                    r.setCategory(data[3].trim());
                    r.setAddress(data[4].trim());

                    // SAFE cost parsing (important)
                    r.setCostForTwo(parseDoubleSafe(
                            data.length > 12 ? data[12] : "0"
                    ));

                    restaurantList.add(r);

                } catch (Exception e) {
                    System.out.println("Skipping bad row: " + line);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private double parseDoubleSafe(String value) {
        try {
            if (value == null) return 0.0;
            return Double.parseDouble(value.trim());
        } catch (Exception e) {
            return 0.0;
        }
    }

    private int parseIntSafe(String value) {
        try {
            if (value == null) return 0;
            return Integer.parseInt(value.trim());
        } catch (Exception e) {
            return 0;
        }
    }

    // ================= DTO MAPPER =================
    private RestaurantResponse mapToResponse(Restaurant r) {
        return new RestaurantResponse(
                r.getRestaurantName(),
                r.getRating(),
                r.getTotalReviews(),
                r.getCategory(),
                r.getAddress(),
                r.getCostForTwo(),
                r.getRating() * r.getTotalReviews()
        );
    }

    // ================= BASIC =================

    public List<Restaurant> getAllRestaurants() {
        return restaurantList;
    }

    // ================= SEARCH =================

    public List<Restaurant> searchByName(String name) {
        return restaurantList.stream()
                .filter(r -> r.getRestaurantName()
                        .toLowerCase()
                        .contains(name.toLowerCase()))
                .collect(Collectors.toList());
    }

    // ================= TRENDING =================

    public List<RestaurantResponse> getTrending(int limit) {
    return restaurantList.stream()
            .sorted((a, b) -> Double.compare(
                    b.getRating() * b.getTotalReviews(),
                    a.getRating() * a.getTotalReviews()
            ))
            .limit(limit > 0 ? limit : 10)
            .map(this::mapToResponse)
            .toList();
    }

    // ================= CAFES =================

    public List<Restaurant> getCafes() {
        return restaurantList.stream()
                .filter(r -> r.getCategory() != null &&
                        r.getCategory().toLowerCase().contains("cafe"))
                .collect(Collectors.toList());
    }

    // ================= DATE NIGHT =================

    public List<Restaurant> getDateNight() {
        return restaurantList.stream()
                .filter(r -> r.getRating() >= 4.2)
                .sorted((a, b) -> Double.compare(b.getRating(), a.getRating()))
                .limit(10)
                .collect(Collectors.toList());
    }

    // ================= AREA =================

    public List<Restaurant> getByArea(String area) {
        return restaurantList.stream()
                .filter(r -> r.getAddress() != null &&
                        r.getAddress().toLowerCase().contains(area.toLowerCase()))
                .collect(Collectors.toList());
    }

    // ================= BUDGET =================

    public List<Restaurant> getBudgetLow() {
        return restaurantList.stream()
                .filter(r -> r.getCostForTwo() <= 300)
                .sorted((a, b) -> Double.compare(b.getRating(), a.getRating()))
                .toList();
    }

    public List<Restaurant> getBudgetMid() {
        return restaurantList.stream()
                .filter(r -> r.getCostForTwo() > 300 && r.getCostForTwo() <= 800)
                .sorted((a, b) -> Double.compare(b.getRating(), a.getRating()))
                .toList();
    }

    public List<Restaurant> getBudgetHigh() {
        return restaurantList.stream()
                .filter(r -> r.getCostForTwo() > 800)
                .sorted((a, b) -> Double.compare(b.getRating(), a.getRating()))
                .toList();
    }

    // ================= BEST VALUE =================

    public List<Restaurant> getBestValue() {
        return restaurantList.stream()
                .sorted((a, b) -> {
                    double scoreA = (a.getRating() * a.getTotalReviews()) / (a.getCostForTwo() + 1);
                    double scoreB = (b.getRating() * b.getTotalReviews()) / (b.getCostForTwo() + 1);
                    return Double.compare(scoreB, scoreA);
                })
                .limit(10)
                .toList();
    }

    // ================= ADVANCED SEARCH =================

    public List<RestaurantResponse> searchRestaurants(
            String name,
            String area,
            String budget,
            String category
    ) {
        return restaurantList.stream()

                .filter(r -> name == null ||
                        r.getRestaurantName().toLowerCase().contains(name.toLowerCase()))

                .filter(r -> area == null ||
                        r.getAddress().toLowerCase().contains(area.toLowerCase()))

                .filter(r -> category == null ||
                        r.getCategory().toLowerCase().contains(category.toLowerCase()))

                .filter(r -> {
                    if (budget == null) return true;

                    double cost = r.getCostForTwo();

                    return switch (budget.toLowerCase()) {
                        case "low" -> cost <= 300;
                        case "mid" -> cost > 300 && cost <= 800;
                        case "high" -> cost > 800;
                        default -> true;
                    };
                })

                .map(this::mapToResponse)
                .toList();
    }

    public List<Restaurant> getSimilarRestaurants(String name) {

    Restaurant target = restaurantList.stream()
            .filter(r -> r.getRestaurantName()
                    .equalsIgnoreCase(name))
            .findFirst()
            .orElse(null);

    if (target == null) {
        return new ArrayList<>();
    }

    return restaurantList.stream()

            .filter(r ->
                    !r.getRestaurantName().equalsIgnoreCase(name))

            .filter(r ->
                    r.getCategory().equalsIgnoreCase(target.getCategory()))

            .sorted((a, b) -> Double.compare(
                    Math.abs(a.getRating() - target.getRating()),
                    Math.abs(b.getRating() - target.getRating())
            ))

            .limit(10)

            .toList();
    }
}