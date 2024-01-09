import React, { useEffect, useState } from "react";
import { Text, SafeAreaView, ScrollView } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { getToken } from "../../../utils/sessionCalls";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";
import EmptyPage from "../../../components/EmptyPage";
import MyEventsPage from "../../../components/MyEventsPage";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;
export default function ListPage() {
  const [isOrganizer, setIsOrganizer] = useState(false);
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

      setIsOrganizer(
        response.role === UserRoles.ORGANIZER_ADMIN ||
          response.role === UserRoles.ORGANIZER,
      );
    });
  }, []);

  return (
    <Container>
      {isNotLogged ? (
        <EmptyPage
          title="You are not logged in"
          subtitle="To see the events you are registered in you should log in first."
          image={require("../../../assets/not-logged-in.png")}
        />
      ) : (
        <ScrollView>
          {isOrganizer ? (
            <Text>This is the screen for the organizers</Text>
          ) : (
            <MyEventsPage />
          )}
        </ScrollView>
      )}
    </Container>
  );
}
