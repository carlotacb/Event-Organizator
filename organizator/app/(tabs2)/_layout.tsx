import React from "react";
import { Tabs } from "expo-router";
import { FontAwesome } from "@expo/vector-icons";

export default () => {
  return (
    <Tabs>
      <Tabs.Screen
        name="ajustes"
        options={{
          tabBarLabel: "Ajustes",
          headerTitle: "Ajustes",
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="gear" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="hackers"
        options={{
          tabBarLabel: "Hackers",
          headerTitle: "Hackathon participants",
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="users" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="stats"
        options={{
          tabBarLabel: "Stats",
          headerTitle: "Stats",
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="pie-chart" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
};
