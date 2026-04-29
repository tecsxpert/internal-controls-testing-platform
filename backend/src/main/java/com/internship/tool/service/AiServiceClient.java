package com.internship.tool.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.http.*;
import java.util.Map;

@Service
public class AiServiceClient {

    private static final Logger logger = LoggerFactory.getLogger(AiServiceClient.class);

    private final RestTemplate restTemplate;

    @Value("${ai.service.url:http://localhost:5000}")
    private String aiServiceUrl;

    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // ── /describe ────────────────────────────────────────────
    public Map describe(Map<String, Object> payload) {
        return callAiService("/describe", payload);
    }

    // ── /recommend ───────────────────────────────────────────
    public Map recommend(Map<String, Object> payload) {
        return callAiService("/recommend", payload);
    }

    // ── /generate-report ─────────────────────────────────────
    public Map generateReport(Map<String, Object> payload) {
        return callAiService("/generate-report", payload);
    }

    // ── Core method ──────────────────────────────────────────
    private Map callAiService(String endpoint, Map<String, Object> payload) {
        try {
            String url = aiServiceUrl + endpoint;
            logger.info("Calling AI service: {}", url);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(payload, headers);

            ResponseEntity<Map> response = restTemplate.exchange(
                url,
                HttpMethod.POST,
                request,
                Map.class
            );

            logger.info("AI service responded with status: {}", response.getStatusCode());
            return response.getBody();

        } catch (ResourceAccessException e) {
            logger.error("AI service timeout or unavailable at {}: {}", endpoint, e.getMessage());
            return null;

        } catch (Exception e) {
            logger.error("AI service call failed at {}: {}", endpoint, e.getMessage());
            return null;
        }
    }
}