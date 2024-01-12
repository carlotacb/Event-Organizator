import { View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import React, { useEffect, useState } from "react";
import { getMyApplications } from "../utils/api/axiosApplications";
import EmptyPage from "./EmptyPage";
import { getToken } from "../utils/sessionCalls";
import LoadingPage from "./LodingPage";
import CardMyEvents from "./CardMyEvents";
import { ApplicationInformationWithoutUser } from "../utils/interfaces/Applications";

const CardsContainer = styled(View)`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  flex-direction: row;
  margin: 20px 0;
`;

export default function MyEventsPage() {
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<ApplicationInformationWithoutUser[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      return getMyApplications(token || "");
    };

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.applications || []);
    });
  }, []);

  return (
    <View>
      {loading ? (
        <LoadingPage />
      ) : (
        <View>
          {events.length === 0 ? (
            <EmptyPage
              title="You have no events"
              subtitle="Go back to homepage to see all our available events!"
              image={require("../assets/empty.png")}
            />
          ) : (
            <CardsContainer>
              {events.map((event: ApplicationInformationWithoutUser) => (
                <CardMyEvents
                  key={event.id}
                  title={event.event.name}
                  headerImage={event.event.header_image}
                  startDate={event.event.start_date}
                  status={event.status}
                />
              ))}
            </CardsContainer>
          )}
        </View>
      )}
    </View>
  );
}
