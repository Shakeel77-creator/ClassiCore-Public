package com.classicore.dto;

import java.util.List;

public class ClassificationResponse {
    private String status;
    private List<PredictionResult> data;

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public List<PredictionResult> getData() {
        return data;
    }

    public void setData(List<PredictionResult> data) {
        this.data = data;
    }
}
