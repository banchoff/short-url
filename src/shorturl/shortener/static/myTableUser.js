const headers = ['First Name', 'Last Name', 'Username', 'Email', 'Actions'];
const data = [];

class MyTable extends React.Component {
    constructor(props) {
	super();
	this.state = {
	    data: props.initialData,
	    next: -1,
	    prev: -1,
	    last: -1,
	    first: 1,
	    current: 1,
	};
	this.updateTable = this.updateTable.bind(this);
    }
    updateTable(e) {
	// If e is null, then this function is being called as updateTable(), meaning
	// it should retrieve again the current page (maybe because an item was added or deleted)
	let pageNum = this.state.current
	let myTable = this
	if (e != null) {
	    switch (e.target.id) {
	    case "btnFirst":
		pageNum = 1;
		break;
	    case "btnPrev":
		pageNum = this.state.prev;
		break;
	    case "btnNext":
		pageNum = this.state.next;
		break;
	    case "btnLast":
		pageNum = this.state.last
		break
	    default:
		console.log("Warning: button not recognised.");
	    }
	}
	
	$.ajax({
	    url: loadUsersAjax,
	    type: 'post',
	    data: {
		'pageNum': pageNum,
		'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	    },
	    success: function(response){
		myTable.setState({
		    data: response.data,
		    next: response.next,
		    prev: response.prev,
		    last: response.last,
		    first: 1,
		    current: response.current,
		})
	    },
	    error: function(response){
		alert("Error loading new data.")
	    }
	});      
    }
    render() {
	return (
		<div>
		<table className="table table-striped">
		<thead>
		<tr> 
		{
		    this.props.headers.map((title, idx) => {
			return <th key={idx}>{title}</th>
		    }
					  )}
	    </tr>
		</thead>
		{this.state.data.length === 0 ? (
		 	<tbody>
			<tr>
			<td colSpan={this.props.headers.length}>
			There are no URLs.
			</td>
			</tr>
			</tbody>
		) : (
			<tbody>
			{/* Keys should be unique. If not, we will have problems when deleting. It does not matter whether they have different IDs, they must have different KEYs. */}
		    {this.state.data.map((row, idx) => (
			    <tr key={row.id}>
			    <td>{row.first_name}</td>
			    <td>{row.last_name}</td>
			    <td>{row.username}</td>
			    <td><a href={`mailto:${row.email}`}>{row.email}</a></td>
			    <td>
			    <button
			data-user-id={`${row.id }`}
			type="button"
			className="btn btn-outline-primary toggleUserAdminButton"
			id={`toggleUserAdminButton-${row.id}`}>
			    {row.is_superuser ? ( "Drop admin" ) : ( "Make admin" )}</button>
			    
			    <button
			data-user-id={`${row.id}`}
			type="button"
			className="btn btn-outline-info changePasswordModalButton"
			data-bs-toggle="modal"
			data-bs-target="#changePasswordUserModal">Change password</button>  
			    
			    <button
			data-user-id={`${row.id}`}
			data-user-username={`${row.username}`}
			type="button"
			className="btn btn-outline-danger deleteUserModalButton"
			data-bs-toggle="modal"
			data-bs-target="#deleteUserModal"
			id={`deleteUserModalButton-${row.id}`}>Delete</button>
			    
			
			</td>
			    </tr>
		    ))}
		    
		    </tbody>
		)}
	    </table>
		<div>
		<button id="btnFirst" className="btn btn-outline-primary btn-sm" onClick={this.updateTable}>First</button>
		<button id="btnPrev" className="btn btn-outline-primary btn-sm" onClick={this.updateTable}>Prev</button>
		{/*<button id="btnCurrent" className="btn btn-outline-primary" onClick={this.updateTable}>Current</button>*/}
		<span>{' '}Page {this.state.current} of {this.state.last}{' '}</span>
		<button id="btnNext" className="btn btn-outline-primary btn-sm" onClick={this.updateTable}>Next</button>
		<button id="btnLast" className="btn btn-outline-primary btn-sm" onClick={this.updateTable}>Last</button>
		</div>
		</div>
	);
    }
}
let myTable = ReactDOM.render(
	<MyTable headers={headers} initialData={data} />,
    document.getElementById('tableContainer'),
);
myTable.updateTable()
