package com.menulytics.backend.dto;

public class RestaurantResponse {

    private String name;
    private double rating;
    private int totalReviews;
    private String category;
    private String address;
    private double costForTwo;
    private double trendingScore;

    public RestaurantResponse(String name, double rating, int totalReviews,
                               String category, String address,
                               double costForTwo, double trendingScore) {
        this.name = name;
        this.rating = rating;
        this.totalReviews = totalReviews;
        this.category = category;
        this.address = address;
        this.costForTwo = costForTwo;
        this.trendingScore = trendingScore;
    }

    public String getName() { return name; }
    public double getRating() { return rating; }
    public int getTotalReviews() { return totalReviews; }
    public String getCategory() { return category; }
    public String getAddress() { return address; }
    public double getCostForTwo() { return costForTwo; }
    public double getTrendingScore() { return trendingScore; }
}