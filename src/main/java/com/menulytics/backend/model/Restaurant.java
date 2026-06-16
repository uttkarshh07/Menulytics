package com.menulytics.backend.model;

import jakarta.persistence.*;

@Entity
@Table(name = "restaurants")
public class Restaurant {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "restaurant_name", nullable = false)
    private String restaurantName;

    @Column(name = "rating")
    private Double rating;

    @Column(name = "total_reviews")
    private Integer totalReviews;

    @Column(name = "category")
    private String category;

    @Column(name = "address")
    private String address;

    @Column(name = "phone")
    private String phone;

    @Column(name = "website")
    private String website;
    
    private double costForTwo;

    // Constructors
    public Restaurant() {
    }

    public Restaurant(String restaurantName, Double rating, Integer totalReviews,
                      String category, String address, String phone, String website) {
        this.restaurantName = restaurantName;
        this.rating = rating;
        this.totalReviews = totalReviews;
        this.category = category;
        this.address = address;
        this.phone = phone;
        this.website = website;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRestaurantName() {
        return restaurantName;
    }

    public void setRestaurantName(String restaurantName) {
        this.restaurantName = restaurantName;
    }

    public Double getRating() {
        return rating;
    }

    public void setRating(Double rating) {
        this.rating = rating;
    }

    public Integer getTotalReviews() {
        return totalReviews;
    }

    public void setTotalReviews(Integer totalReviews) {
        this.totalReviews = totalReviews;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getWebsite() {
        return website;
    }

    public void setWebsite(String website) {
        this.website = website;
    }

    public double getCostForTwo() {
    return costForTwo;
}

    public void setCostForTwo(double costForTwo) {
    this.costForTwo = costForTwo;
}
}
