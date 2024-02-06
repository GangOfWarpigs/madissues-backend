package org.madissues.core.infraestructure;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Requester {
    public static void main(String[] args) throws URISyntaxException, IOException, InterruptedException {
       HttpRequest request = HttpRequest.newBuilder()
               .GET()
               .uri(new URI("https://catfact.ninja/fact"))
               .build();

       var joke = getJsonObject(request, JsonObject.class);
       System.out.println(joke.get("fact"));
    }

    private static <T> T getJsonObject(HttpRequest request, Class<T> classObject) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newBuilder().build();
        var response = client.send(request, HttpResponse.BodyHandlers.ofString());
        var json = new Gson().fromJson(response.body(), classObject);
        return json;
    }
}
