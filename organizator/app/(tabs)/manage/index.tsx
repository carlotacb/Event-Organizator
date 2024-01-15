import React, { useEffect, useState } from "react";
import { SafeAreaView, ScrollView } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import Toast from "react-native-toast-message";
import { getToken } from "../../../utils/sessionCalls";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";
import EmptyPage from "../../../components/Pages/EmptyPage";
import MyEventsPage from "../../../components/Pages/MyEventsPage";
import OrganizersEventsPage from "../../../components/Pages/OrganizersEventsPage";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;
export default function ListPage() {
  const [isOrganizer, setIsOrganizer] = useState(false);
  const [isParticipant, setIsParticipant] = useState(false);
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
      setIsParticipant(response.role === UserRoles.PARTICIPANT);
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
        <ScrollView contentContainerStyle={{ padding: 20 }}>
          {isOrganizer && <OrganizersEventsPage />}
          {isParticipant && <MyEventsPage />}
        </ScrollView>
      )}
      <Toast />
    </Container>
  );
}
