package com.classicore.service;

import com.classicore.dto.ClassificationResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Service
public class ClassifierService {

    private final WebClient webClient;

    @Value("${classifier.base-url}")
    private String baseUrl;

    public ClassifierService() {
        this.webClient = WebClient.builder().build();
    }

    public ClassificationResponse classify(String productName) {
        return webClient.post()
                .uri(baseUrl + "/api/classify/")
                .bodyValue(Map.of("product_name", productName))
                .retrieve()
                .bodyToMono(ClassificationResponse.class)
                .block();
    }
}

