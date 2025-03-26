
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';
const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);
  const { id } = useParams();
    /*
  const root_url = window.location.origin + "/";
  const dealer_url = `${root_url}djangoapp/dealer/${id}/`;
  const reviews_url = `${root_url}djangoapp/reviews/dealer/${id}/`;
  const post_review_url = `${root_url}postreview/${id}`;
  const baseURL = "https://jsswp199427-3030.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/";
    */
  const baseURL = "https://jsswp199427-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/";
  const dealer_url = `${baseURL}djangoapp/dealer/${id}`;
  const reviews_url = `${baseURL}djangoapp/reviews/dealer/${id}/`;
  const post_review_url = `${baseURL}postreview/${id}`;
  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();
      if (retobj.status === 200) {
        const data = Array.isArray(retobj.dealer) ? retobj.dealer[0] : retobj.dealer;
        setDealer(data || {});
      }
    } catch (error) {
      console.error("Error fetching dealer:", error);
    }
  };
  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url);
      const retobj = await res.json();
      if (retobj.status === 200) {
        if (retobj.reviews.length > 0) {
          setReviews(retobj.reviews);
        } else {
          setUnreviewed(true);
        }
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };
  const senti_icon = (sentiment) => {
    return sentiment === "positive"
      ? positive_icon
      : sentiment === "negative"
      ? negative_icon
      : neutral_icon;
  };
  useEffect(() => {
   // console.log("✅ Dealer component mounted");
   // console.log("Fetching dealer from:", dealer_url);
   // console.log("Fetching reviews from:", reviews_url);
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review_url}>
          <img
            src={review_icon}
            style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }}
            alt='Post Review'
          />
        </a>
      );
    }
  }, []);
  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1>Dealer Loaded: {dealer?.full_name || "None"}</h1>
        <h1 style={{ color: "grey" }}>
          {dealer?.full_name || "Loading Dealer..."} {postReview}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer?.city}, {dealer?.address}, Zip - {dealer?.zip}, {dealer?.state}
        </h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <p>Loading Reviews...</p>
        ) : unreviewed ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review, idx) => (
            <div className="review_panel" key={idx}>
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt="Sentiment"
              />
              <div className="review">{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
export default Dealer;
