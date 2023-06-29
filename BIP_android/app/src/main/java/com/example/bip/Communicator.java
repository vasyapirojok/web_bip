package com.example.bip;

import androidx.navigation.fragment.NavHostFragment;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class Communicator {
    JSONObject obj;
    private static String url = "";
    private String cookie = "";

    public int Register(String email, String password) {

        String salt;

        try {
            URL url = new URL("http://172.20.10.10:8001/signup_salt_app");

            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            String jsonInputString = "{\"email\": \"" + email + "\"}";
            OutputStream os = con.getOutputStream();
            os.write(jsonInputString.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) { //success
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                JSONObject jsonObject = new JSONObject(response.toString());
                if (jsonObject.get("available").toString().equals("0")) {
                    return 2; // already in use
                }

                salt = jsonObject.get("salt").toString();

            } else {
                return responseCode;
            }
        } catch (Exception e) {
            return 1; // unknown error
        }

//        send creds
        try {
            URL url = new URL("http://172.20.10.10:8001/signup_creds_app");

            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            String hash = Hash256String(password + salt);

            String jsonInputString = "{\"email\": \"" + email + "\", \"hash_password\": \"" + hash + "\"}";
            OutputStream os = con.getOutputStream();
            os.write(jsonInputString.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) { //success
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

            } else {
                return responseCode;
            }
        } catch (Exception e) {
            return 1; // unknown error
        }


        return 0;
    }

    public int Login(String email, String password) {

        String salt;

        try {
            URL url = new URL("http://172.20.10.10:8001/login_salt_app");

            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            String jsonInputString = "{\"email\": \"" + email + "\"}";
            OutputStream os = con.getOutputStream();
            os.write(jsonInputString.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) { //success
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                JSONObject jsonObject = new JSONObject(response.toString());
                if (jsonObject.get("available").toString().equals("0")) {
                    return 2; // invalid creds
                }

                salt = jsonObject.get("salt").toString();

            } else {
                return responseCode;
            }
        } catch (Exception e) {
            return 1; // unknown error
        }

//        send creds
        try {
            URL url = new URL("http://172.20.10.10:8001/login_creds_app");

            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            String hash = Hash256String(password + salt);

            String jsonInputString = "{\"email\": \"" + email + "\", \"hash_password\": \"" + hash + "\"}";
            OutputStream os = con.getOutputStream();
            os.write(jsonInputString.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) { //success
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                JSONObject jsonObject = new JSONObject(response.toString());
                if (!jsonObject.get("status").toString().equals("OK")) {
                    return 2; // invalid creds
                }

            } else {
                return responseCode;
            }
        } catch (Exception e) {
            return 1; // unknown error
        }


        return 0;
    }

    public int VerifyCode(String email, String code){

        String salt;

        try {
            URL url = new URL("http://172.20.10.10:8001/check_code_app");

            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            String jsonInputString = "{\"email\": \"" + email + "\", \"code\": \"" + code + "\"}";
            OutputStream os = con.getOutputStream();
            os.write(jsonInputString.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) { //success
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                JSONObject jsonObject = new JSONObject(response.toString());

                String token = jsonObject.get("token").toString();
                if (token.isEmpty()) {
                    return 2; // incorrect code
                }

                cookie = token;

                return 0;

            } else {
                return responseCode;
            }
        } catch (Exception e) {
            return 1; // unknown error
        }
    }
    private static String Hash256String(String data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedhash = digest.digest(
                    data.getBytes(StandardCharsets.UTF_8));
            return bytesToHex(encodedhash);
        }catch (Exception e) {
            return new String("");
        }
    }

    private static String bytesToHex(byte[] hash) {
        StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (int i = 0; i < hash.length; i++) {
            String hex = Integer.toHexString(0xff & hash[i]);
            if(hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }

    public int ReqRacio(int price, int days, String shop){

        String salt;


        try {
            URL url = new URL("http://172.20.10.10:8001/get_page_app");

            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            String jsonInputString = "{\"page_number\": 1, \"shops_list\": [\""+ shop + "\"]}";
            OutputStream os = con.getOutputStream();
            os.write(jsonInputString.getBytes());
            os.flush();
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("GET Response Code :: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) { //success
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                JSONObject jsonObject = new JSONObject(response.toString());
                obj = jsonObject;

                return 0;

            } else {
                return responseCode;
            }
        } catch (Exception e) {
            return 1; // unknown error
        }
    }

    public JSONObject getJsonObject() {
        return obj;
    }
}
