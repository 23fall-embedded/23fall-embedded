package com.example.backend;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class test {
    @RequestMapping("/toJson")
    @ResponseBody
    public Map<String, String> toJson(){

        Map<String,String> map= new HashMap<String,String>();
        map.put("name","wang");

        return map;

    }

}
