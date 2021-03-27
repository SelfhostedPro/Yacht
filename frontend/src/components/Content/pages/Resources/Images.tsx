import React, { useEffect } from "react";
import { useFetch } from "../../../../utils";

const Images = () => {
  const { data, error, loading } = useFetch("/api/resources/images/");

  useEffect(() => {
    error && console.log(error);
    // data && console.log(data);
  }, [error]);

  return (
    <>
      <div className={"text-2xl"}>IMAGES</div>
      <div>
        {loading ? (
          <span>loading...</span>
        ) : (
          <span>
            whoa! Thats a lot of data for {data && data.length} objects...
          </span>
        )}
      </div>
    </>
  );
};

export default Images;
