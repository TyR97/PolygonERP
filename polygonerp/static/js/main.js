function confirmUpdate() {
  return confirm("Are you sure you want to update this worker’s data?");
}

function projectCreated(){
  alert("Project created successfully!");
  window.location.href = "{{ url_for('dashboard.dashboard', user_id=session['id']) }}";
}

function confirmDelete(){
  const checkbox = document.getElementById("terminatedCheckbox");

  if(checkbox.checked){
    return true;
  }

  return confirm("Are you sure you want to delete this worker if the contract is NOT terminated?");;
}