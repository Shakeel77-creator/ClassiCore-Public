package com.classicore.dto;

public class PredictionResult {
    private String input_phrase;
    private String predicted_code;
    private String matched_name;
    private double elapsed;
    private String raw_output;
    private String source;
    private double confidence;

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getInput_phrase() {
        return input_phrase;
    }

    public void setInput_phrase(String input_phrase) {
        this.input_phrase = input_phrase;
    }

    public String getPredicted_code() {
        return predicted_code;
    }

    public void setPredicted_code(String predicted_code) {
        this.predicted_code = predicted_code;
    }

    public String getMatched_name() {
        return matched_name;
    }

    public void setMatched_name(String matched_name) {
        this.matched_name = matched_name;
    }

    public double getElapsed() {
        return elapsed;
    }

    public void setElapsed(double elapsed) {
        this.elapsed = elapsed;
    }

    public String getRaw_output() {
        return raw_output;
    }

    public void setRaw_output(String raw_output) {
        this.raw_output = raw_output;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }
}
