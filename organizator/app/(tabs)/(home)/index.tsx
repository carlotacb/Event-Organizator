import React, { useEffect, useState } from "react";
import { Pressable, SafeAreaView, ScrollView, View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { router } from "expo-router";
import { useIsFocused } from "@react-navigation/core";
import { EventAllInformation } from "../../../utils/interfaces/Events";
import {
  getAllEvents,
  getAllUpcomingEvents,
} from "../../../utils/api/axiosEvents";
import CardHomePage from "../../../components/componentsStyled/Cards/CardHomePage";
import LoadingPage from "../../../components/Pages/LodingPage";
import EmptyPage from "../../../components/Pages/EmptyPage";
import { getToken } from "../../../utils/sessionCalls";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";
import FilterButton from "../../../components/componentsStyled/Buttons/FilterButtons";
import {
  BottomScreenContainer,
  CardsContainer,
  FiltersContainer,
} from "../../../components/componentsStyled/Shared/ContainerStyles";
import Button from "../../../components/componentsStyled/Buttons/ButtonWithIcon";
import { systemColors } from "../../../components/componentsStyled/tokens";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<EventAllInformation[]>([]);
  const [futureEvents, setFutureEvents] = useState<EventAllInformation[]>([]);
  const [allEvents, setAllEvents] = useState<EventAllInformation[]>([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [active, setActive] = useState({
    all: false,
    past: false,
    future: true,
  });

  const isFocused = useIsFocused();

  useEffect(() => {
    const fetchData = async () => getAllUpcomingEvents();
    const fetchAllEvents = async () => getAllEvents();
    const fetchAdminFunction = async () => {
      const t = await getToken();
      return getUserRole(t);
    };

    fetchData().then((response) => {
      setLoading(false);
      setActive({ all: false, past: false, future: true });
      setEvents(response.eventInformation || []);
      setFutureEvents(response.eventInformation || []);
    });

    fetchAllEvents().then((response) => {
      setAllEvents(response.eventInformation || []);
    });

    fetchAdminFunction().then((response) => {
      setIsAdmin(response.role === UserRoles.ORGANIZER_ADMIN);
    });
  }, [isFocused]);

  return (
    <Container>
      <ScrollView contentContainerStyle={{ paddingHorizontal: 10 }}>
        {loading ? (
          <LoadingPage />
        ) : (
          <View>
            <FiltersContainer>
              <FilterButton
                title="All"
                onPress={() => {
                  setActive({ all: true, past: false, future: false });
                  setEvents(allEvents);
                }}
                color="#040240"
                iconName="list"
                active={active.all}
              />
              <FilterButton
                title="Past"
                onPress={() => {
                  setActive({ all: false, past: true, future: false });
                  setEvents(
                    allEvents.filter(
                      (e) => e.start_date < new Date().toISOString(),
                    ),
                  );
                }}
                color="#040240"
                iconName="calendar-times-o"
                active={active.past}
              />
              <FilterButton
                title="Future"
                onPress={() => {
                  setActive({ all: false, past: false, future: true });
                  setEvents(futureEvents);
                }}
                color="#040240"
                iconName="calendar"
                active={active.future}
              />
            </FiltersContainer>
            <View style={{ justifyContent: "center" }}>
              {events.length === 0 ? (
                <EmptyPage
                  title="There are no events"
                  subtitle="Come back in a few days... maybe we have news!"
                  image={require("../../../assets/empty.png")}
                />
              ) : (
                <CardsContainer>
                  {events.map((event) => (
                    <Pressable
                      onPress={() => {
                        router.push(`/${event.id}`);
                      }}
                      key={event.id}
                    >
                      <CardHomePage
                        title={event.name}
                        startDate={event.start_date}
                        endDate={event.end_date}
                        location={event.location}
                        id={event.id}
                        headerImage={event.header_image}
                        isStudent={event.students_only}
                      />
                    </Pressable>
                  ))}
                </CardsContainer>
              )}
            </View>
          </View>
        )}
      </ScrollView>
      {isAdmin && (
        <BottomScreenContainer>
          <Button
            title="Create new"
            onPress={() => {
              router.push("/create");
            }}
            color={systemColors.action}
          />
        </BottomScreenContainer>
      )}
    </Container>
  );
}
