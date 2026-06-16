package com.menulytics.backend.repository;

import com.menulytics.backend.model.Restaurant;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RestaurantRepository extends JpaRepository<Restaurant, Long> {

    List<Restaurant> findByRestaurantNameContainingIgnoreCase(String name);

}