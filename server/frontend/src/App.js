import LoginPanel from "./components/Login/Login";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer"; // ✅ Newly added
import PostReview from "./components/Dealers/PostReview"
import { Routes, Route } from "react-router-dom";

function App() {
  return (
        <div style={{ padding: "20px", border: "2px solid red" }}>
      
      <Routes>
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/dealers" element={<Dealers />} />
        <Route path="/dealer/:id" element={<Dealer />} />
        <Route path="/postreview/:id" element={<PostReview/>} />
      </Routes>
    </div>
    

  );
}

export default App;

/*
function App() {
    return (
      <div style={{ padding: "50px", backgroundColor: "gold" }}>
        <h1>💡 React App Rendered!</h1>
      </div>
    );
  }
  
export default App;
*/