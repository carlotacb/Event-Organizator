import { Pressable, Text, View } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import React from "react";
// @ts-ignore
import styled from "styled-components/native";
import InformativeChip from "../Chips/InformativeChip";

const UserLine = styled(View)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  border-bottom-width: 1px;
  border-bottom-color: #e6e6e6;
`;

const Username = styled(Text)`
  font-weight: bold;
  font-size: 15px;
`;

const ButtonAndRole = styled(View)`
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: center;
`;

interface ListLineProps {
  id: string;
  name: string;
  chipColor: string;
  role: string;
  setAlertVisible: any;
  setIdLine: any;
  setMoreInfoFromLine: any;
  iconName?: any;
}

export default function ListLine(props: ListLineProps) {
  const {
    id,
    name,
    role,
    chipColor,
    setAlertVisible,
    setIdLine,
    setMoreInfoFromLine,
    iconName,
  } = props;

  return (
    <UserLine>
      <Username>{name}</Username>
      <ButtonAndRole>
        <InformativeChip
          name={role}
          backgroundColor={chipColor}
          fontSize="12px"
          notBold
        />
        {iconName && (
          <Pressable
            onPress={() => {
              setAlertVisible(true);
              setIdLine(id);
              setMoreInfoFromLine(name);
            }}
          >
            <FontAwesome name={iconName} size={18} />
          </Pressable>
        )}
      </ButtonAndRole>
    </UserLine>
  );
}
