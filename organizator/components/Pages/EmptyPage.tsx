import { Image, View } from "react-native";
import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import { SubTitle, Title } from "../componentsStyled/TextStyles";

interface EmptyPageProps {
  title: string;
  subtitle: string;
  image: any;
}

const NoEventsContainer = styled(View)`
  padding: 100px 50px;
  align-items: center;
`;

export default function EmptyPage(props: EmptyPageProps) {
  const { title, subtitle, image } = props;

  return (
    <NoEventsContainer>
      <Title>{title}</Title>
      <SubTitle>{subtitle}</SubTitle>
      <Image
        source={image}
        style={{ width: 280, height: 280, alignSelf: "center", marginTop: 40 }}
      />
    </NoEventsContainer>
  );
}
