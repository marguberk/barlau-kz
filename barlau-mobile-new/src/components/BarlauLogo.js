import React from 'react';
import { View } from 'react-native';
import Svg, { Rect } from 'react-native-svg';

export default function BarlauLogo({ width = 42, height = 23 }) {
  return (
    <View style={{ width, height }}>
      <Svg width={width} height={height} viewBox="0 0 42 23">
        {/* Три синие полоски логотипа BARLAU.KZ */}
        <Rect x="0" y="2" width="32" height="3" fill="#2679DB" rx="1.5" />
        <Rect x="0" y="9" width="28" height="3" fill="#2679DB" rx="1.5" />
        <Rect x="0" y="16" width="24" height="3" fill="#2679DB" rx="1.5" />
      </Svg>
    </View>
  );
} 
 
 
 
 