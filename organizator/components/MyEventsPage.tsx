import { ScrollView, View } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import React, { useEffect, useState } from "react";
import Toast from "react-native-toast-message";
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
  const [applications, setApplications] = useState<
    ApplicationInformationWithoutUser[]
  >([]);
  const [trigger, setTrigger] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const token = await getToken();
      return getMyApplications(token || "");
    };

    fetchData().then((response) => {
      setLoading(false);
      setApplications(response.applications || []);
    });
  }, [trigger]);

  return (
    <View>
      {loading ? (
        <LoadingPage />
      ) : (
        <ScrollView>
          {applications.length === 0 ? (
            <EmptyPage
              title="You have no events"
              subtitle="Go back to homepage to see all our available events!"
              image={require("../assets/empty.png")}
            />
          ) : (
            <CardsContainer>
              {applications.map(
                (application: ApplicationInformationWithoutUser) => (
                  <CardMyEvents
                    key={application.id}
                    title={application.event.name}
                    headerImage={application.event.header_image}
                    startDate={application.event.start_date}
                    status={application.status}
                    id={application.id}
                    trigger={trigger}
                    setTrigger={setTrigger}
                  />
                ),
              )}
            </CardsContainer>
          )}
        </ScrollView>
      )}
      <Toast />
    </View>
  );
}
