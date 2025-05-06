package com.classicore.controller;

import com.classicore.dto.ClassificationResponse;
import com.classicore.service.ClassifierService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/classify")
@CrossOrigin
public class ClassificationController {

    @Autowired
    private ClassifierService classifierService;

    @PostMapping
    public ClassificationResponse classify(@RequestBody Map<String, String> request) {
        return classifierService.classify(request.get("product_name"));
    }
}
