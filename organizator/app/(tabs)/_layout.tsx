import React from "react";
import { Tabs } from "expo-router";
import { FontAwesome5 } from "@expo/vector-icons";

export default function HomepageTabs() {
  return (
    <Tabs>
      <Tabs.Screen
        name="(home)"
        options={{
          tabBarLabel: "Home",
          headerTitle: "All upcoming events",
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome5 name="home" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="list"
        options={{
          tabBarLabel: "News",
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome5 name="newspaper" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          tabBarLabel: "Profile",
          headerTitle: "My profile",
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome5 name="user" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
}
