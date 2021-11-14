# Usage: pass in the DB container ID as the argument

# Set database configurations
export CT_DB_USERNAME=ct_admin
export CT_DB_NAME=geoconnections


kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME -c 'Select * FROM public.location';"
