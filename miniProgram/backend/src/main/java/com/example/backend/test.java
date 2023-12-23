package com.example.backend;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

import static java.lang.Integer.parseInt;

@RestController
public class test {
    @RequestMapping("/toJson")
    @ResponseBody
    public Map<String, String> toJson(){

        Map<String,String> map= new HashMap<String,String>();
        map.put("name","wang");

        return map;

    }

    @RequestMapping("/LED")
    public void getLEDinfo(HttpServletRequest request, HttpServletResponse response){
        int id = parseInt(request.getParameter("LEDid"));
        System.out.println(id);
    }

}
