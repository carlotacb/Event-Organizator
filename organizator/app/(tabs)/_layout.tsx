import React, { useEffect, useState } from "react";
import { Tabs } from "expo-router";
import { FontAwesome } from "@expo/vector-icons";
import { getToken } from "../../utils/sessionCalls";
import { getUserRole } from "../../utils/api/axiosUsers";
import { UserRoles } from "../../utils/interfaces/Users";

export default function HomepageTabs() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [isNotLogged, setIsNotLogged] = useState(false);

  useEffect(() => {
    const fetchAdminFunction = async () => {
      const t = await getToken();
      return getUserRole(t);
    };

    fetchAdminFunction().then((response) => {
      if (response.error) {
        setIsNotLogged(true);
        return;
      }
      setIsAdmin(response.role === UserRoles.ORGANIZER_ADMIN);
    });
  }, []);

  return (
    <Tabs>
      <Tabs.Screen
        name="(home)"
        options={{
          tabBarLabel: "Home",
          headerTitle: "All upcoming events",
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="home" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="list"
        options={{
          tabBarLabel: "News",
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="list" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          tabBarLabel: isNotLogged ? "Login" : "Profile",
          headerTitle: "My profile",
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome
              name={isNotLogged ? "sign-in" : "user"}
              color={color}
              size={size}
            />
          ),
        }}
      />
    </Tabs>
  );
}
