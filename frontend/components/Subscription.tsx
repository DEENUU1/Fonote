
const Subscription = () => {
    return (
        <>
            <h1>Subscription</h1>
            <div className='subscription'>
                <div className='starter-div' >
                    <h2>Starter plan</h2>
                    <img className='month-img' src='https://img.freepik.com/free-vector/subscriber-concept-illustration_114360-3453.jpg?t=st=1654685116~exp=1654685716~hmac=b67fdd003003bc4f477b5184b2201a36a5a88ebefc2552ee7f4f723a2acef85f&w=740'></img>

                    <form action={`http://localhost:8000/api/subscription/create/`} method="POST">
                        <input type="hidden" name="price_id" value="price_1P6vSVE3z5SG6L41bej8QhXE" />
                        <button className="btn-month" type="submit" >&#8377;30 / Month</button>
                    </form>
                </div>
                <br></br>
            </div>
            <br>
            </br>
        </>
    );
}

export default Subscription;