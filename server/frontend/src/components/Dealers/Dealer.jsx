import React, { useEffect } from "react";
import { useParams } from "react-router-dom";

function Dealer() {
  const { id } = useParams();

  useEffect(() => {
    console.log("✅ React mounted at /dealer/" + id);
  }, [id]);

  return (
    <div style={{ backgroundColor: "lightblue", padding: "40px" }}>
      <h2>✅ React is working</h2>
      <p>Dealer ID from URL: <strong>{id}</strong></p>
    </div>
  );
}

export default Dealer;
